import json
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PIL import Image as PilImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf'))  # 请将这里的'simhei.ttf'替换为你字体文件的实际路径

def create_pdf_from_json(input_json_path, output_pdf_path):
    with open(input_json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    Story=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Chinese', fontName='SimHei', fontSize=12)) # 添加新的ParagraphStyle

    for page_num, content in data.items():
        text = content.get('translation', '')
        images = content.get('img', [])

        # Add text
        text = '<font name="SimHei">{}</font>'.format(text) # 使用SimHei字体
        Story.append(Paragraph(text, styles["Chinese"])) # 使用新的ParagraphStyle

        # Add images
        for img_path in images:
            # Create ReportLab Image from PIL image
            img = PilImage.open(img_path)
            img_width, img_height = img.size
            aspect = img_height / float(img_width)
            Story.append(Image(img_path, width=doc.width, height=doc.width*aspect))
            
        Story.append(PageBreak()) # 插入一个分页符，确保每个json字典对应一页PDF

    doc.build(Story)

def main():
    create_pdf_from_json('output-translated.json', 'output.pdf')

if __name__ == '__main__':
    main()
