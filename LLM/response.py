import json
import re


def parse_response(response):
    # 尝试多种可能的 JSON 包装格式
    json_patterns = [
        r'```json\s*(.*?)\s*```',  # 标准 Markdown JSON 块
        r'```\s*({\s*"APIs_with_options".*?})\s*```',  # 没有指定 json 的代码块
        r'({?\s*"APIs_with_options".*?})\s*',  # 可能没有代码块包装的 JSON
    ]

    json_str = None
    for pattern in json_patterns:
        match = re.search(pattern, response, re.DOTALL)
        if match:
            json_str = match.group(1)
            break

    if not json_str:
        raise ValueError("No JSON-like data found in the response")

    try:
        # 尝试解析 JSON 字符串
        data = json.loads(json_str)
    except json.JSONDecodeError:
        # 如果解析失败，尝试修复常见问题
        json_str = json_str.replace("'", '"')  # 将单引号替换为双引号
        json_str = re.sub(r'(\w+):', r'"\1":', json_str)  # 给键名加上引号
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON after attempted fixes: {e}")

    # 提取 APIs_with_options 数据
    apis_with_options = data.get('APIs_with_options', {})
    if not apis_with_options:
        raise ValueError("No 'APIs_with_options' found in the parsed data")

    # 转换数据格式
    result = {}
    for api_name, options_list in apis_with_options.items():
        api_options = []
        if not isinstance(options_list, list):
            options_list = [options_list]  # 如果不是列表，将其转换为列表

        for option in options_list:
            if not isinstance(option, dict):
                continue  # 跳过非字典项

            param_index = option.get('param_index')
            options = option.get('options')

            if param_index is None or options is None:
                continue  # 跳过缺少必要键的项

            # 处理范围值
            if isinstance(options, str):
                range_match = re.search(r'range:\s*(\d+)-(\d+)', options)
                if range_match:
                    start, end = map(int, range_match.groups())
                    options = f"range: {start}-{end}"
                else:
                    options = options.strip()
            elif not isinstance(options, list):
                options = [str(options)]  # 将非列表选项转换为单项列表

            api_options.append({
                'param_index': param_index,
                'options': options
            })

        if api_options:  # 只添加非空的 API 选项
            result[api_name] = api_options

    return result


def parse_driver_response(response):
    # 尝试多种可能的 JSON 包装格式
    json_patterns = [
        r'```json\s*(.*?)\s*```',  # 标准 Markdown JSON 块
        r'```\s*({\s*"fuzz_driver".*?})\s*```',  # 没有指定 json 的代码块
        r'({?\s*"fuzz_driver".*?})\s*',  # 可能没有代码块包装的 JSON
    ]

    json_str = None
    for pattern in json_patterns:
        match = re.search(pattern, response, re.DOTALL)
        if match:
            json_str = match.group(1)
            break

    if not json_str:
        raise ValueError("No JSON-like data found in the response")

    try:
        # 尝试解析 JSON 字符串
        data = json.loads(json_str)
    except json.JSONDecodeError:
        # 如果解析失败，尝试修复常见问题
        json_str = json_str.replace("'", '"')  # 将单引号替换为双引号
        json_str = re.sub(r'(\w+):', r'"\1":', json_str)  # 给键名加上引号
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON after attempted fixes: {e}")

    # 提取 fuzz_driver 数据
    fuzz_driver = data.get('fuzz_driver', {})
    if not fuzz_driver:
        raise ValueError("No 'fuzz_driver' found in the parsed data")

    return fuzz_driver