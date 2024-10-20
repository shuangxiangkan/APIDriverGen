from Parser.C.markdown_search import search_markdown_files
from Util.Classify import FileClassifier
from Parser.C.C_Collect import collect_caller_comment_info
from Parser.C.C_Parser import C_Parser_Builder
from Parser.C.C_API import APIInfo, ParameterInfo, TypeInfo, CallerInfo, MentionedInfo, MarkdownInfo


class CLibraryAnalyzer:
    def __init__(self, library_path, header_paths, api_prefix=''):
        self.library_path = library_path
        self.header_paths = header_paths
        self.parser = C_Parser_Builder('c').build()
        self.apis = {}  # Dictionary to store all API information
        self.types = {}  # Dictionary to store all type information
        self.api_prefix = api_prefix

    def parse(self):
        self.parse_headers()
        self.collect_additional_info()

    def parse_headers(self, api_filter='', comment_location='above'):
        for header_path in self.header_paths:
            self._parse_file(header_path, api_filter, comment_location)

    def _parse_file(self, file_path, api_filter, comment_location):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        tree = self.parser.parse(bytes(content, 'utf8'))
        self._extract_info(tree.root_node, content, file_path, api_filter, comment_location)

    def _extract_info(self, node, content, file_path, api_filter, comment_location):
        if node.type in ['declaration']:
            api_info = self._extract_api_info(node, content, file_path, comment_location)
            if api_info and (api_filter in api_info.signature or api_filter in api_info.comment):
                self.apis[api_info.name] = api_info  # Store API info in dictionary
        if node.type == 'preproc_def':
            define_info = self._extract_define_info(node, content, comment_location)
            if define_info:
                self.types[define_info.name] = define_info
        if node.type == 'type_definition':
            type_name = node.child_by_field_name('declarator')
            type_node = node.child_by_field_name('type')
            if type_name and type_node:
                type_info = self._extract_type_info(type_node, content, comment_location)
                if type_info:
                    self.types[type_name.text.decode('utf8')] = type_info
        elif node.type in ['struct_specifier', 'enum_specifier']:
            type_info = self._extract_type_info(node, content, comment_location)
            if type_info:
                self.types[type_info.name] = type_info
        else:
            for child in node.children:
                self._extract_info(child, content, file_path, api_filter, comment_location)

    def _extract_api_info(self, node, content, file_path, comment_location):
        declarator = node.child_by_field_name('declarator')
        if not declarator:
            return None

        name = self._get_function_name(declarator)

        # Check if the API name matches the prefix
        if self.api_prefix and not name.startswith(self.api_prefix):
            return None

        signature = content[node.start_byte:node.end_byte].split('{')[0].strip()
        comment = self._find_comment(node, content, comment_location)

        api_info = APIInfo(name, signature, comment, file_path, node.start_point[0] + 1)

        # Extract parameter information
        params = self._get_function_parameters(declarator)
        for param in params:
            param_name = param['name']
            param_type = self._get_or_create_type(param['type'], content)
            api_info.add_parameter(ParameterInfo(param_name, param_type))

        # Extract return type information
        return_type = node.child_by_field_name('type')
        if return_type:
            return_type_info = self._get_or_create_type(return_type.text.decode('utf8'), content)
            api_info.add_return_type(return_type_info)

        return api_info

    def _extract_type_info(self, node, content, comment_location):
        name = node.child_by_field_name('name')
        if not name:
            name = ""
        else:
            name = name.text.decode('utf8')
        kind = node.type.split('_')[0]  # 'struct', 'enum', or 'typedef'
        definition = content[node.start_byte:node.end_byte]
        comment = self._find_comment(node, content, comment_location)

        return TypeInfo(name, kind, definition, comment)

    def _extract_define_info(self, node, content, comment_location):
        name = node.child_by_field_name('name').text.decode('utf8')
        value = node.child_by_field_name('value')
        definition = f"#define {name} {value.text.decode('utf8') if value else ''}"
        comment = self._find_comment(node, content, comment_location)

        return TypeInfo(name, 'define', definition, comment)

    def _get_or_create_type(self, type_name, content):
        if type_name in self.types:
            return self.types[type_name]
        else:
            # Create a basic TypeInfo for unknown types
            return TypeInfo(type_name, 'unknown', type_name, '')

    def _get_function_name(self, declarator):
        if declarator.type == 'function_declarator':
            return declarator.child_by_field_name('declarator').text.decode('utf8')
        return declarator.text.decode('utf8')

    def _get_function_parameters(self, declarator):
        params = []
        parameter_list = declarator.child_by_field_name('parameters')
        if parameter_list:
            for param in parameter_list.children:
                if param.type == 'parameter_declaration':
                    param_type = param.child_by_field_name('type').text.decode('utf8')
                    param_name = param.child_by_field_name('declarator')
                    param_name = param_name.text.decode('utf8') if param_name else ''
                    params.append({'name': param_name, 'type': param_type})
        return params

    def _find_comment(self, node, content, comment_location):
        if comment_location == 'above':
            return self._find_comment_before_node(node, content)
        elif comment_location == 'below':
            return self._find_comment_after_node(node, content)
        else:
            return self._find_comment_before_node(node, content) or self._find_comment_after_node(node, content)

    def _find_comment_before_node(self, node, content):
        start_line = node.start_point[0]
        lines = content.split('\n')
        comment_lines = []

        for i in range(start_line - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith('//') or line.startswith('/*'):
                comment_lines.insert(0, line)
            elif line.endswith('*/'):
                comment_lines.insert(0, line)
                while i > 0:
                    i -= 1
                    line = lines[i].strip()
                    comment_lines.insert(0, line)
                    if line.startswith('/*'):
                        break
            else:
                break

        return '\n'.join(comment_lines)

    def _find_comment_after_node(self, node, content):
        end_byte = node.end_byte
        lines = content[end_byte:].split('\n')
        comment_lines = []

        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if i == 0 and not stripped_line:
                continue  # Skip the first empty line if it exists
            if stripped_line.startswith('//'):
                comment_lines.append(stripped_line)
            elif stripped_line.startswith('/*'):
                comment_lines.append(stripped_line)
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    comment_lines.append(next_line)
                    if '*/' in next_line:
                        break
                break
            elif stripped_line:
                break  # Stop if we encounter any non-comment content

        return '\n'.join(comment_lines)

    def collect_additional_info(self):
        classifier = FileClassifier()
        classifier.categorize_files(self.library_path)
        c_cpp_files = classifier.get_c_cpp_files()
        markdown_files = classifier.get_markdown_files()

        api_names = self.apis.keys()

        # Collect caller and mentioned info
        all_calls, all_comments = collect_caller_comment_info(c_cpp_files, api_names, self.parser)
        for api_name, info_list in all_calls.items():
            for info in info_list:
                self.apis[api_name].caller_info.append(CallerInfo(info["file"], info["code"]))

        for api_name, info in all_comments.items():
            for comment in info:
                self.apis[api_name].mentioned_info.append(MentionedInfo(comment["file"], comment["comment"]))

        # Collect markdown info
        markdown_info = search_markdown_files(markdown_files, api_names)
        for api_name, info_list in markdown_info.items():
            for info in info_list:
                self.apis[api_name].markdown_info.append(MarkdownInfo(info["file"], info["context"]))

    def get_all_apis(self):
        return self.apis

    def get_all_types(self):
        return self.types

    def get_api_by_name(self, name):
        return self.apis.get(name)