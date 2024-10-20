from Util.Print import ColorPrint
import random

class TypeInfo:
    def __init__(self, name, kind, definition, comment):
        self.name = name
        self.kind = kind  # 'struct', 'enum', 'define', etc.
        self.definition = definition
        self.comment = comment

    def get_comment_and_definition(self):
        return f"{self.comment}\n{self.definition}"

    def __str__(self):
        return (f"Name: {ColorPrint.yellow(self.name)}\n"
                f"Kind: {ColorPrint.cyan(self.kind)}\n"
                f"Definition: {ColorPrint.green(self.definition)}\n"
                f"Comment: {ColorPrint.blue(self.comment)}")

class ParameterInfo:
    def __init__(self, name, type_info):
        self.name = name
        self.type_info = type_info

    def __str__(self):
        return (f"Name: {ColorPrint.yellow(self.name)}\n"
                f"Type: {ColorPrint.green(self.type_info.name)}")

class CallerInfo:
    def __init__(self, file_path, caller_code):
        self.file_path = file_path
        self.caller_code = caller_code

    def __str__(self):
        return (f"File: {ColorPrint.yellow(self.file_path)}\n"
                f"Code: {ColorPrint.green(self.caller_code)}")

class MentionedInfo:
    def __init__(self, file_path, mentioned_comment):
        self.file_path = file_path
        self.mentioned_comment = mentioned_comment

    def __str__(self):
        return (f"File: {ColorPrint.yellow(self.file_path)}\n"
                f"Mentioned Comment: {ColorPrint.green(self.mentioned_comment)}")

class MarkdownInfo:
    def __init__(self, file_path, markdown_info):
        self.file_path = file_path
        self.markdown_info = markdown_info

    def __str__(self):
        return (f"File: {ColorPrint.red(self.file_path)}\n"
                f"Markdown Info: {ColorPrint.green(self.markdown_info)}")


class APIInfo:
    def __init__(self, name, signature, comment, file_path, line_number):
        self.name = name
        self.signature = signature
        self.comment = comment
        self.parameters = []
        self.return_type = None
        self.caller_info = [] # List of caller methods (CallerInfo) that call this API
        self.mentioned_info = [] # List of comments (MentionedInfo, except API signature comment) that mention this API
        self.markdown_info = [] # List of markdown info (MarkdownInfo) that mention this API
        self.file_path = file_path
        self.line_number = line_number

    def add_parameter(self, param):
        self.parameters.append(param)

    def add_return_type(self, return_type):
        self.return_type = return_type

    # Get all unique types involved in this API, only include the types that are define in the self_defined_types
    # self_defined_types: a set of type names that are defined in the library
    def get_involved_types(self, self_defined_types=None):
        if self_defined_types is None:
            self_defined_types = set()

        # Collect all unique types
        unique_types = set()
        for param in self.parameters:
            if self_defined_types is None or param.type_info.name in self_defined_types:
                unique_types.add(param.type_info)
        if self.return_type and (self_defined_types is None or self.return_type.name in self_defined_types):
            unique_types.add(self.return_type)

        return unique_types

    def get_caller_info(self):
        return self.caller_info

    def get_mentioned_info(self):
        return self.mentioned_info

    def get_markdown_info(self):
        return self.markdown_info

    # Get all unique types involved in this API, and its comment and definition
    def get_detailed_info_str(self, self_defined_types=None):
        # Involved types
        involved_types = self.get_involved_types(self_defined_types)
        type_info_str = "\n".join([f"{type_info.get_comment_and_definition()}\n" for type_info in involved_types])

        return (f"{type_info_str}\n"
                f"{self.comment}\n"
                f"{self.signature}\n")

    # # 随机选择3个示例
    # def get_usage_examples(self):
    #     usage_examples = ""
    #
    #     # 如果示例数量超过3个，随机选择3个
    #     if len(self.caller_info) > 3:
    #         selected_callers = random.sample(self.caller_info, 3)
    #     else:
    #         selected_callers = self.caller_info
    #
    #     for index, caller in enumerate(selected_callers, 1):
    #         usage_examples += f"Example {index}:\n"
    #         usage_examples += f"\n{caller.caller_code}\n\n"
    #
    #     return usage_examples

    def get_usage_examples(self):
        usage_examples = ""

        # 如果示例数量超过3个，选择最短的3个
        if len(self.caller_info) > 3:
            selected_callers = sorted(self.caller_info, key=lambda x: len(x.caller_code))[:3]
        else:
            selected_callers = self.caller_info

        for index, caller in enumerate(selected_callers, 1):
            usage_examples += f"Example {index}:\n"

            # 将代码分割成行
            code_lines = caller.caller_code.split('\n')

            # 找到self.name的位置
            self_name_index = next(i for i, line in enumerate(code_lines) if self.name in line)

            # 如果总行数不超过30行，则完全保留
            if len(code_lines) <= 30:
                usage_examples += f"\n{caller.caller_code}\n\n"
            else:
                # 计算开始和结束的索引
                start_index = max(0, self_name_index - 19)  # 尽量保留前20行
                end_index = min(len(code_lines), self_name_index + 11)  # 尽量保留后10行

                # 如果结束索引超出范围，调整开始索引
                if end_index > len(code_lines):
                    start_index = max(0, len(code_lines) - 30)
                    end_index = len(code_lines)

                # 提取所需的代码行
                selected_code = '\n'.join(code_lines[start_index:end_index])

                # 添加省略号表示被截断的部分
                if start_index > 0:
                    selected_code = "...\n" + selected_code
                if end_index < len(code_lines):
                    selected_code += "\n..."

                usage_examples += f"\n{selected_code}\n\n"

        return usage_examples

    def get_additional_info(self):
        additional_info = ""
        for markdown_info, index in zip(self.markdown_info, range(len(self.markdown_info))):
            additional_info += f"Additional Info {index + 1}:\n"
            additional_info += f"\n{markdown_info.markdown_info}\n\n"

        return additional_info

    def __str__(self):
        params_str = "\n".join([f"  - {param}" for param in self.parameters])
        return_str = f"Return Type: {self.return_type}" if self.return_type else "Return Type: None"

        return (f"API Name: {ColorPrint.red(self.name)}\n"
                f"Signature: {ColorPrint.green(self.signature)}\n"
                f"Comment: {ColorPrint.blue(self.comment)}\n"
                f"Parameters:\n{params_str}\n"
                f"{return_str}\n"
                f"File: {self.file_path}:{self.line_number}")