from Parser.C.C_Info import CLibraryAnalyzer
from LLM.chatgpt import call_gpt
from LLM.prompts import get_APIs_with_options_prompt



# Usage example:
if __name__ == "__main__":
    library_path = "/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/cJSON"
    header_paths = ["/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/cJSON/cJSON.h"]
    # library_path = "/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/miniz"
    # header_paths = ["/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/miniz/miniz.h"]
    # library_path = "/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/zlib"
    # header_paths = ["/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/zlib/zlib.h"]
    # library_path = "/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/libtiff/libtiff"
    # header_paths = ["/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/libtiff/libtiff/tiffio.h"]
    # library_path = "/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/libjpeg-turbo"
    # header_paths = ["/Users/shuangxiangkan/Code/PycharmProject/APIDriverGen/Libraries/libjpeg-turbo/src/turbojpeg.h"]

    analyzer = CLibraryAnalyzer(library_path, header_paths)
    # api_filter = "ZEXPORT"
    # comment_location = 'below'
    # analyzer.parse_headers(api_filter, comment_location)
    analyzer.parse_headers()
    # analyzer.parse_headers()
    analyzer.print_all_apis()
    # analyzer.print_all_apis_with_detailed_info()
    # analyzer.print_all_types()
    # api_info = analyzer.get_api_signatures_and_comments()
    # print(api_info)
    api_sig_info = analyzer.get_api_signatures()
    print(api_sig_info)

    # APIs_with_options_prompt = get_APIs_with_options_prompt(api_info)
    # gpt_response = call_gpt(APIs_with_options_prompt)
    # print(gpt_response)