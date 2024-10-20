import re
import markdown
from bs4 import BeautifulSoup


def search_markdown_files(markdown_files, api_names):
    results = {}

    for file_path in markdown_files:
        if file_path.endswith('.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()

                # 将Markdown转换为HTML
                html_content = markdown.markdown(md_content)

                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(html_content, 'html.parser')

                # 提取所有文本内容
                text_content = soup.get_text()

                for api_name in api_names:
                    # 使用正则表达式搜索API名称
                    matches = re.finditer(rf'\b{re.escape(api_name)}\b', text_content, re.IGNORECASE)

                    for match in matches:
                        start = max(0, match.start() - 300)
                        end = min(len(text_content), match.end() + 300)
                        context = text_content[start:end]

                        if api_name not in results:
                            results[api_name] = []

                        results[api_name].append({
                            'file': file_path,
                            'context': context.strip()
                        })

            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

    return results