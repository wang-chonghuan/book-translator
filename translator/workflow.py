from s1_extract_pdf import extract_content_from_pdf
from s2_translate_content import translate_pdf_content
from s3_create_pdf import create_pdf_from_json

def main_workflow(pdf_file_path, start_page):
    base_name = pdf_file_path.split(".")[0]  # 从pdf文件名获取基本名字（不包括扩展名）
    img_folder_path = base_name + "-images"  # 创建一个以基本名字为基础的文件夹来存储图片
    formatted_json_file_path = base_name + "-formatted.json"  # 格式化json文件的名称
    translated_json_file_path = base_name + "-translated.json"  # 翻译json文件的名称
    output_pdf_file_path = base_name + "-translated.pdf"  # 翻译pdf文件的名称

    # 第一步：从PDF提取内容并保存为JSON
    extract_content_from_pdf(pdf_file_path, img_folder_path, formatted_json_file_path)

    # 第二步：将JSON内容翻译为中文
    translate_pdf_content(formatted_json_file_path, translated_json_file_path, start_page)

    # 第三步：使用翻译的JSON内容创建PDF
    create_pdf_from_json(translated_json_file_path, output_pdf_file_path)

if __name__ == '__main__':
    main_workflow('.\data\Fashion_and_Lies-Marisa_Marmo.pdf', '1')
