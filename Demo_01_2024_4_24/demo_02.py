import os
from xml.etree.ElementTree import Element, SubElement, ElementTree

def safe_open(file_path):
    try:
        # 尝试使用 UTF-8 编码打开文件
        return open(file_path, 'r', encoding='gb2312', errors='ignore')
    except UnicodeDecodeError:
        # 如果 UTF-8 失败，尝试使用 GBK 编码
        return open(file_path, 'r', encoding='gbk')

def txt_to_xml(directory, output_file):
    # 创建 XML 的根元素
    root = Element('documents')

    # 遍历目录中的所有 txt 文件
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            path = os.path.join(directory, filename)
            with safe_open(path) as file:
                lines = file.readlines()
                title = lines[0].strip()
                content = ''.join(lines[1:]).strip()

                # 创建一个文档元素
                document = SubElement(root, 'document')
                SubElement(document, 'title').text = title
                SubElement(document, 'content').text = content

    # 生成 XML 树并保存
    tree = ElementTree(root)
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)

# 使用示例
directory = './CJFD/'
output_xml = 'output.xml'
txt_to_xml(directory, output_xml)
