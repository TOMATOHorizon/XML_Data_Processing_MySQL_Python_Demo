def read_multiple_specific_lines(file_path, line_numbers):
    line_numbers_set = set(line_numbers)  # 将行号列表转换为集合以提高查找效率
    lines_content = {}
    with open(file_path, 'r', encoding='GB2312', errors='ignore') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number in line_numbers_set:
                lines_content[current_line_number] = line.strip()
            if len(lines_content) == len(line_numbers_set):  # 如果已经读取了所有指定行，提前结束
                break
    return lines_content

# 使用示例
file_path = './CJFD/CJFD2005.txt'
line_numbers = [3966]  # 假设你想读取第3行和第5行
character_position = 1983
lines_content = read_multiple_specific_lines(file_path, line_numbers)
for number, content in lines_content.items():
    string_List = list(content)
    print(f"第{number}行的内容是: {content}")
    print(len(string_List))
    for i in range(9):
        print(f"第{character_position + i}个字符是：'{string_List[character_position - 1 + i]}'")
