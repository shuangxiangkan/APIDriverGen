file_extensions = ['.c', '.cpp', '.h', '.hpp']

def parse_function_info(file_path, api_names, parser):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = parser.parse(bytes(code, 'utf8'))
    root_node = tree.root_node

    function_info = {api_name: {'calls': [], 'comments': []} for api_name in api_names}

    def traverse(node):
        if node.type == 'call_expression':
            func_name = node.child_by_field_name('function').text.decode('utf8')
            if func_name in api_names:
                # Find the outermost function definition
                parent = node
                while parent is not None and parent.type != 'function_definition':
                    parent = parent.parent
                if parent is not None:
                    function_info[func_name]['calls'].append({
                        'code': code[parent.start_byte:parent.end_byte],
                        'file': file_path
                    })

        elif node.type == 'comment':
            comment_text = node.text.decode('utf8')
            for api_name in api_names:
                if api_name in comment_text:
                    # Merge consecutive comments
                    start_byte = node.start_byte
                    end_byte = node.end_byte
                    # Merge upwards
                    prev_node = node.prev_sibling
                    while prev_node and prev_node.type == 'comment':
                        start_byte = prev_node.start_byte
                        prev_node = prev_node.prev_sibling
                    # Merge downwards
                    next_node = node.next_sibling
                    while next_node and next_node.type == 'comment':
                        end_byte = next_node.end_byte
                        next_node = next_node.next_sibling
                    full_comment = code[start_byte:end_byte]
                    function_info[api_name]['comments'].append({
                        'comment': full_comment,
                        'file': file_path
                    })

        for child in node.children:
            traverse(child)

    traverse(root_node)
    return function_info

def collect_caller_comment_info(file_list, api_names, parser):
    all_calls = {api_name: [] for api_name in api_names}
    all_comments = {api_name: [] for api_name in api_names}

    for file_path in file_list:
        if any(file_path.endswith(ext) for ext in file_extensions):
            function_info = parse_function_info(file_path, api_names, parser)
            for api_name in api_names:
                all_calls[api_name].extend(function_info[api_name]['calls'])
                all_comments[api_name].extend(function_info[api_name]['comments'])

    return all_calls, all_comments