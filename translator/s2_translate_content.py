import openai
import json
import time

openai.api_key = "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"

def translate_pdf_content(json_file_path, output_file_path, start_page):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 获取所有页面，并进行排序
    pages = sorted(data.keys(), key=lambda x: int(x))

    # 找到开始页的索引
    start_index = pages.index(start_page)

    for page in pages[start_index:]:
        content = data[page]
        text = content['text']
        message = [{"role": "user", "content": text + "\n-------------------------------------\n请把上述文本翻译成中文, 不要添加或删除任何内容. 然后把翻译的结果格式化成html, 代码放在合适的标签里. 最后只返回给我这个html, 其他任何额外的东西都不要返回给我"}]

        while True:
            try:
                print(f"sending message: {message}")
                chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message)
                translation = chat_completion.choices[0].message.content
                data[page]['translation'] = translation

                # 打印翻译结果
                print(f"Page {page} translated: {translation}")

                # 在每次翻译完成后，立即更新JSON文件
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    json.dump(data, output_file, ensure_ascii=False, indent=4)
                break
            except Exception as e:
                print(f"An exception occurred: {e}")
                print("Retrying...")
                time.sleep(1)  # 这个延迟是可选的，可以根据实际情况增加或删除

def main():
    translate_pdf_content('output.json', 'output-translated.json', '1')

if __name__ == "__main__":
    main()
