from Parser.C.C_Info import CLibraryAnalyzer
from LLM.chatgpt import call_gpt
from LLM.prompts import get_APIs_with_options_prompt, generate_fuzz_driver_prompt
from LLM.response import parse_response, parse_driver_response
from Util.Classify import FileClassifier
from Util.Print import ColorPrint
from libfuzzer2afl.libfuzzer2afl import libfuzzer2afl


def print_all_api_signatures(apis):
    for api in apis.values():
        print(api.signature)
        print("-" * 50)

def print_all_types(types):
    for type in types:
        type_info = types[type].get_comment_and_definition()
        print(type_info)

def get_all_api_comments_and_signatures(apis):
    api_info = ""
    for api in apis.values():
        api_info += f"{api.comment}\n{api.signature}\n\n"
    return api_info

def get_APIs_with_options(apis_info):
    APIs_with_options_prompt = get_APIs_with_options_prompt(apis_info)
    gpt_response = call_gpt(APIs_with_options_prompt)
    # print(gpt_response)

    parse_results = parse_response(gpt_response)
    for api_name, options_list in parse_results.items():
        print(f"API: {api_name}")
        for option in options_list:
            print(f"Param Index: {option['param_index']}")
            print(f"Options: {option['options']}")
        print("-" * 50)

    print(f"\n\nThere are {len(parse_results)} APIs with options.")

def get_fuzz_driver(api):
    param_types_and_return_type = api.get_involved_types()
    api_signature = api.signature
    comments = api.comment
    usage_examples = api.get_usage_examples()
    additional_info = api.get_additional_info()

    fuzz_driver_prompt = generate_fuzz_driver_prompt(param_types_and_return_type, api_signature, comments, usage_examples, additional_info)
    gpt_response = call_gpt(fuzz_driver_prompt)
    # print(gpt_response)

    parse_results = parse_driver_response(gpt_response)
    afl_driver = libfuzzer2afl(parse_results)
    print(f"{ColorPrint.red(afl_driver)}")


# Usage example:
if __name__ == "__main__":
    library_path = "/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/cJSON"
    header_paths = ["/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/cJSON/cJSON.h"]

    analyzer = CLibraryAnalyzer(library_path, header_paths)
    # analyzer.parse_headers()
    analyzer.parse()

    # all_apis = analyzer.get_all_apis()
    # # print_all_api_signatures(all_apis)
    #
    # all_types = analyzer.get_all_types()
    # # print_all_types(all_types)

    api = analyzer.get_api_by_name("cJSON_ParseWithLength")

    get_fuzz_driver(api)

    # caller_info = api.get_caller_info()
    # for caller in caller_info:
    #     print(f"File: {ColorPrint.yellow(caller.file_path)}")
    #     print("Code:")
    #     print(caller.caller_code)
    #     print("-" * 80)

    # mentioned_info = api.get_mentioned_info()
    # for comment in mentioned_info:
    #     print(f"File: {ColorPrint.yellow(comment.file_path)}")
    #     print("Comment:")
    #     print(comment.mentioned_comment)
    #     print("-" * 80)

    # markdown_info = api.get_markdown_info()
    # for markdown in markdown_info:
    #     print(f"File: {ColorPrint.yellow(markdown.file_path)}")
    #     print("Markdown Info:")
    #     print(markdown.markdown_info)
    #     print("-" * 80)