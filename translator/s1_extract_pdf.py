#pip install PyMuPDF pillow
import fitz  # pip install PyMuPDF
import io
import os
import json
from PIL import Image  # pip install pillow


def extract_content_from_pdf(pdf_file_path, img_folder_path, json_file_path):
    # 如果 images 文件夹不存在，创建新的文件夹
    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)
    doc = fitz.open(pdf_file_path)
    data_dict = {}

    for i in range(len(doc)):
        page = doc.load_page(i)  # number of page
        image_list = page.get_images(full=True)
        img_paths = []

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]

            # Save the image data to a file
            img_file_path = f'{img_folder_path}/page-{i+1}-img-{img_index}.png'
            with open(img_file_path, 'wb') as img_file:
                img_file.write(image_data)
            img_paths.append(img_file_path)

        text = page.get_text("text")

        data_dict[str(i + 1)] = {"text": text, "img": img_paths}

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


def main():
    # Ensure images folder exists
    if not os.path.exists('images'):
        os.makedirs('images')
    # Run the extraction
    extract_content_from_pdf('sample-farm-35.pdf', 'images', 'output.json')


if __name__ == "__main__":
    main()

"""
该Python程序的主要功能是从指定的PDF文件中提取每页的文本和图片内容。对于每一页，它都将抽取所有的文本和所有的图片。所有的图片会被保存到一个指定的文件夹中，并且每个图片的文件名会指明它是来自于哪一页以及它在该页的索引位置。

最终，所有的这些信息会被存储到一个JSON文件中，其格式如下：

json
Copy code
{
  "1": {
    "text": "all text content in this page",
    "img": ["img-0-path", "img-1-path"],
    "translation": "text content translated"
  },
  "2": {
    "text": "all text content in this page",
    "img": ["img-0-path", "img-1-path", "img-2-path"],
    "translation": "text content translated"
  },
  ...
}
每一个键是页码，对应的值是一个字典，该字典包含两个键：

"text": 对应的值是一个字符串，包含了该页的所有文本。
"img": 对应的值是一个列表，包含了该页所有图片的文件路径。路径按照图片在PDF页面上出现的顺序排列。
这个程序对于从PDF文件中提取文本和图片非常有用，尤其是当你需要处理大量的PDF文件并且需要将提取的数据以结构化的方式（如JSON）存储时。
"""