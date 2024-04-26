import mysql.connector
from lxml import etree
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser

# User input for MySQL database connection
def get_database_connection():
    # db_user = input("Enter your MySQL username: ")
    # db_password = input("Enter your MySQL password: ")
    # db_host = input("Enter your MySQL host (default 'localhost'): ") or 'localhost'
    # db_database = input("Enter your database name: ")
    return mysql.connector.connect(
        user='root',
        password='744214Sgg',
        host='localhost',
        database='xml_store_test'
    )

# Setup and populate the database and Whoosh index
def setup_database_and_index(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS literature (
            id VARCHAR(255) PRIMARY KEY, 
            title TEXT, 
            content TEXT
        )
    ''')

    # Parse XML data
    parser = etree.XMLParser(huge_tree=True)
    tree = etree.parse('output.xml', parser)
    root = tree.getroot()

    for article in root.findall('article'):
        id_ = article.find('id').text
        title = article.find('title').text
        content = article.find('content').text
        c.execute('INSERT INTO literature (id, title, content) VALUES (%s, %s, %s)', (id_, title, content))

    conn.commit()

    schema = Schema(title=TEXT(stored=True), content=TEXT)
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    c.execute('SELECT title, content FROM literature')
    for (title, content) in c:
        writer.add_document(title=title, content=content)
    writer.commit()

    c.close()

# Search functionality
def search_literature(query_str):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        for result in results:
            print(result['title'])

def main():
    conn = get_database_connection()
    setup_database_and_index(conn)
    conn.close()

    # Example search
    search_literature("example search term")

if __name__ == "__main__":
    main()
