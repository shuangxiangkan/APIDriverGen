import os
import magic

class FileClassifier:
    def __init__(self):
        # 初始化magic对象
        self.mime = magic.Magic()

        # 定义文件类型类别
        self.categories = {
            'C/C++ files': ['text/x-c', 'text/x-c++src', 'text/x-chdr', 'text/x-c++hdr'],
            'Text files': ['text/plain'],
            'PDF files': ['application/pdf'],
            'DOCX files': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
            'Markdown files': ['text/markdown'],
            'Other files': []
        }

        # 记录分类结果
        self.categorized_files = {
            'C/C++ files': [],
            'Text files': [],
            'PDF files': [],
            'DOCX files': [],
            'Markdown files': [],
            'Other files': []
        }

    def categorize_files(self, directory):
        """遍历目录并根据MIME类型和文件后缀对文件进行分类"""
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_type = self.mime.from_file(file_path)

                categorized = False
                # 通过MIME类型分类
                for category, mime_types in self.categories.items():
                    if any(mime_type in file_type for mime_type in mime_types):
                        self.categorized_files[category].append(file_path)
                        categorized = True
                        break

                # 通过文件后缀名分类
                if not categorized:
                    file_extension = os.path.splitext(file)[1].lower()
                    if file_extension in ['.c', '.cpp', '.h', '.hpp']:
                        self.categorized_files['C/C++ files'].append(file_path)
                    elif file_extension == '.txt':
                        self.categorized_files['Text files'].append(file_path)
                    elif file_extension == '.pdf':
                        self.categorized_files['PDF files'].append(file_path)
                    elif file_extension == '.docx':
                        self.categorized_files['DOCX files'].append(file_path)
                    elif file_extension == '.md':
                        self.categorized_files['Markdown files'].append(file_path)
                    else:
                        self.categorized_files['Other files'].append(file_path)

    def get_c_cpp_files(self):
        """获取C/C++文件列表"""
        return self.categorized_files['C/C++ files']

    def get_text_files(self):
        """获取文本文件列表"""
        return self.categorized_files['Text files']

    def get_pdf_files(self):
        """获取PDF文件列表"""
        return self.categorized_files['PDF files']

    def get_docx_files(self):
        """获取DOCX文件列表"""
        return self.categorized_files['DOCX files']

    def get_markdown_files(self):
        """获取Markdown文件列表"""
        return self.categorized_files['Markdown files']

    def get_other_files(self):
        """获取其他文件列表"""
        return self.categorized_files['Other files']

    def print_categorized_files(self):
        """打印分类后的文件列表"""
        for category, files in self.categorized_files.items():
            print(f"{category}:")
            for file in files:
                print(f"  {file}")
            print("\n")

# 示例用法
# directory = './Libraries/cJSON'  # 这里替换为你的目标文件夹路径
# classifier = FileClassifier()
# classifier.categorize_files(directory)
# classifier.print_categorized_files()