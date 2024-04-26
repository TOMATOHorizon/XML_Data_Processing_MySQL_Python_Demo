import os
import mysql.connector
from lxml import etree
from lxml.etree import XMLParser
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser


def get_database_connection():
    """ Connect to the MySQL database using environment variables for security. """
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '744214Sgg')
    host = os.getenv('MYSQL_HOST', 'localhost')
    database = os.getenv('MYSQL_DATABASE', 'xml_store_test')
    return mysql.connector.connect(user=user, password=password, host=host, database=database)


def setup_database_and_index(conn):
    """ Setup and populate the database and Whoosh index """
    c = conn.cursor()
    try:
        c.execute('''
            CREATE TABLE IF NOT EXISTS literature (
                id VARCHAR(255) PRIMARY KEY,
                title TEXT,
                content TEXT
            )
        ''')
        conn.commit()
    except mysql.connector.Error as e:
        print(f"SQL Error: {e}")
        return

    data_folder = './CJFD/'
    files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.txt')]
    parser = XMLParser(huge_tree=True)

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='gb2312', errors='ignore') as file:
                xml_content = file.read()
                tree = etree.fromstring(xml_content.encode('utf-8'), parser=parser)

                for article in tree.findall('article'):
                    id_ = article.find('id').text
                    title = article.find('title').text
                    content = article.find('content').text
                    c.execute('INSERT INTO literature (id, title, content) VALUES (%s, %s, %s)', (id_, title, content))
            conn.commit()
        except etree.XMLSyntaxError as e:
            print(f"XML Error: {e}")
        except mysql.connector.Error as e:
            print(f"SQL Error during insert: {e}")

    setup_whoosh_index(c)


def setup_whoosh_index(c):
    """ Setup the Whoosh index from the database literature """
    schema = Schema(title=TEXT(stored=True), content=TEXT)
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    try:
        c.execute('SELECT title, content FROM literature')
        for title, content in c:
            writer.add_document(title=title, content=content)
        writer.commit()
    except mysql.connector.Error as e:
        print(f"SQL Error during index creation: {e}")


def search_literature(query_str):
    """ Perform search on Whoosh index """
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        for result in results:
            print(result['title'])


def main():
    """ Main function to establish DB connection and execute functionality """
    conn = get_database_connection()
    setup_database_and_index(conn)
    conn.close()

    # Example search
    search_literature("example search term")


if __name__ == "__main__":
    main()
