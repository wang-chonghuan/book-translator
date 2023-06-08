import json
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file_path, json_file_path):
    # 打开 PDF 文件
    with open(pdf_file_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
        # 准备一个字典用于存储每页的文本
        pages_dict = {}
        # 遍历每一页
        for page_num in range(total_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            # 把这页的文本存储到字典中
            pages_dict[f'page-{page_num+1}'] = text
    # 把字典写入 json 文件
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(pages_dict, json_file, ensure_ascii=False, indent=4)

def main():
    extract_text_from_pdf('sample-farm-17.pdf', 'output.json')

if __name__ == "__main__":
    main()
