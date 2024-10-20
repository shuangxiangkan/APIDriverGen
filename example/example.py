import os
import magic

def classify_files_by_magic(directory):
    # 创建一个Magic对象
    file_magic = magic.Magic(mime=True)  # 设置mime=True以返回MIME类型

    # 创建一个字典来存储不同MIME类型的文件
    mime_dict = {}

    # 遍历目录中的所有文件
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # 只处理文件，忽略目录
        if os.path.isfile(item_path):
            # 获取文件的MIME类型
            mime_type = file_magic.from_file(item_path)
            # 将文件添加到对应的MIME类型列表中
            if mime_type not in mime_dict:
                mime_dict[mime_type] = []
            mime_dict[mime_type].append(item)

    # 打印每种MIME类型对应的文件
    for mime_type, files in mime_dict.items():
        print(f"MIME类型: {mime_type}")
        for file in files:
            print(f"  {file}")
        print()  # 添加一个空行以便于阅读

# 使用示例
directory = './example'
classify_files_by_magic(directory)
