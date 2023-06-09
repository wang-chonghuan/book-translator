import json
import re
import html

def format_translation_to_html(json_input_path, html_output_path):
    with open(json_input_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 正则表达式用于匹配和删除<html>和<body>标签
    html_body_pattern = r'</?html>|</?body>'

    # 正则表达式用于查找<code>...</code>中的内容
    code_pattern = r'<code>(.*?)</code>'

    # 正则表达式用于匹配行级元素和非<p>,<pre>,<code>的块级元素
    line_level_elements_pattern = r'</?(?!p\b|pre\b|code\b|br\b)[a-z][a-z0-9]*[^>]*>'

    # 初始化html内容，开始创建html文件结构
    html_content = '<!DOCTYPE html>\n<html>\n<body>\n'

    for page_num, content in data.items():
        # 获取translation字段的值
        translation = content.get('translation', '')

        # 删除<html>和<body>标签
        translation = re.sub(html_body_pattern, '', translation, flags=re.IGNORECASE)

        # 转义<code>...</code>中的HTML代码
        translation = re.sub(code_pattern, lambda m: f'<code>{html.escape(m.group(1))}</code>', translation, flags=re.DOTALL)

        # 替换所有非行级元素为<p>标签，并移除行级元素
        translation = re.sub(line_level_elements_pattern, '', translation)

        # 确保translation字段的值都位于一个<p></p>标签里
        translation = f'<p>{translation}</p>'

        # 在每个translation之间加上<br>以及其对应的页码
        html_content += f'<p>Page {page_num}</p>\n{translation}<br>\n'

    # 结束创建html文件结构
    html_content += '\n</body>\n</html>'

    # 将html内容写入html文件
    with open(html_output_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

def main():
    format_translation_to_html('output-translated.json', 'output.html')

if __name__ == "__main__":
    main()
