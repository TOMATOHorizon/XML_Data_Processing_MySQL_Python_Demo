import os
import re

from lxml import etree
from lxml.etree import XMLParser


def convert_and_save_xml(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有.txt文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.xml')

            # 创建一个XML解析器，开启huge_tree选项以允许解析大型XML文件
            parser = XMLParser(encoding='gb2312', huge_tree=True, recover=True)

            # 读取并解析XML文件
            with open(input_file_path, 'r', encoding='gb2312', errors='ignore') as file:
                try:
                    content = re.sub(r'<([^=?!][^>]*)>', r'&lt;\1&gt;', file.read())
                    # 解析为XML树的根元素
                    root = etree.fromstring(content.encode('gb2312'), parser=parser)
                    # 使用根元素创建ElementTree对象
                    tree = etree.ElementTree(root)
                    # 现在可以安全地调用write()方法保存XML文件
                    tree.write(output_file_path, encoding='utf-8', xml_declaration=True, pretty_print=True)
                    print(f"Processed and saved: {output_file_path}")
                except etree.XMLSyntaxError as e:
                    print(f"Error processing {input_file_path}: {e}")


# 指定输入和输出文件夹
input_folder = './CJFD/'
output_folder = './After_Treatment_CJFD/'

# 调用函数
convert_and_save_xml(input_folder, output_folder)
