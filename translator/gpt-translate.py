#pip install --upgrade openai
import openai
import json

openai.api_key = ""

def translate_pdf_content(json_file_path, output_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for page, content in data.items():
        text = content['text']
        message = [{"role": "user", "content": text + "-------------------------------------please translate this content into chinese, dont produce or remove anything else"}]
        print(f"sending message: {message}")
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)
        translation = chat_completion.choices[0].message.content
        data[page]['translation'] = translation

        # 打印翻译结果
        print(f"Page {page} translated: {translation}")

        # 在每次翻译完成后，立即更新JSON文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)

def main():
    translate_pdf_content('output.json', 'output-translated.json')

if __name__ == "__main__":
    main()
