

def test_prompt():
    messages = [
        {"role": "system",
         "content": "You are ChatGPT, and you are an expert about programming."},
        {"role": "user",
         "content": (
             "How to parse JSON in C?"
         )
         }
    ]

    return messages

def get_APIs_with_options_prompt(API_signatures_comments):
    messages = [
        {"role": "system",
         "content": "You are ChatGPT, an expert programming assistant."},
        {"role": "user",
         "content": (
             f"Based on the provided API signatures and comments, please identify all APIs that require options to be passed during the function call.\n\n"
             f"API Signatures and Comments:\n{API_signatures_comments}\n\n"
             f"For each API that requires options, please provide the following information:\n"
             f"- API name\n"
             f"- Index of the parameter that requires options (1-based indexing)\n"
             f"- The possible values or range of values for each option parameter\n\n"
             f"Please format the response as a single-line JSON object. "
             f"Wrap the JSON object with Markdown syntax using triple backticks (```). Example format: "
             f"```json {{\"APIs_with_options\": {{\"API_name1\": [{{\"param_index\": 1, \"options\": [\"value1\", \"value2\"]}}], "
             f"\"API_name2\": [{{\"param_index\": 1, \"options\": [\"value1\", \"value2\"]}}, {{\"param_index\": 2, \"options\": \"range: 1-10\"}}]}}}}```. "
             f"For options with a continuous range, use the format 'range: start-end' or 'range: min-max'."
         )}
    ]
    return messages


def generate_fuzz_driver_libfuzzer_prompt(param_types_and_return_type, api_signature, comments, usage_examples, additional_info):
    messages = [
        {"role": "system",
         "content": "You are ChatGPT, an expert in fuzzing and writing libfuzzer fuzz drivers for C/C++ APIs."},
        {"role": "user",
         "content": (
             f"Based on the provided API parameter and return types, comments, signature, usage examples, and additional information, "
             f"please generate a fuzz driver for libfuzzer testing. The driver should correctly call the API, "
             f"maximize efficiency, and incorporate the provided information effectively. "
             f"Make sure to explore all possible options within the API parameters to identify potential bugs "
             f"that may arise from different configurations.\n\n"
             f"API Parameter and Return Types:\n{param_types_and_return_type}\n"
             f"API Comments:\n{comments}\n"
             f"API Signatures:\n{api_signature}\n"
             f"Usage Examples:\n{usage_examples}\n"
             f"Additional Information:\n{additional_info}\n\n"
             f"Please format the response as a single-line JSON object. Wrap the JSON object with Markdown syntax "
             f"using triple backticks (```). Example format: "
             f"```json {{\"fuzz_driver\": \"<generated_code>\"}}```."
         )}
    ]
    return messages

def generate_fuzz_driver_afl_prompt(param_types_and_return_type, api_signature, comments, usage_examples, additional_info):
    messages = [
        {"role": "system",
         "content": "You are ChatGPT, an expert in fuzzing and writing AFL++ fuzz drivers for C/C++ APIs."},
        {"role": "user",
         "content": (
             f"Based on the provided API parameter and return types, comments, signature, usage examples, and additional information, "
             f"please generate a fuzz driver for AFL++ testing. The driver should correctly call the API, "
             f"maximize efficiency, and incorporate the provided information effectively. "
             f"Make sure to explore all possible options within the API parameters to identify potential bugs "
             f"that may arise from different configurations.\n\n"
             f"API Parameter and Return Types:\n{param_types_and_return_type}\n"
             f"API Comments:\n{comments}\n"
             f"API Signatures:\n{api_signature}\n"
             f"Usage Examples:\n{usage_examples}\n"
             f"Additional Information:\n{additional_info}\n\n"
             f"Remember to consider the specific requirements of AFL++ fuzzing and how they may affect the driver.\n\n"
             f"Please format the response as a single-line JSON object. Wrap the JSON object with Markdown syntax "
             f"using triple backticks (```). Example format: "
             f"```json {{\"fuzz_driver\": \"<generated_code>\"}}```."
             f"\n\nRemember to consider the specific requirements of AFL++ fuzzing, not for libfuzzer and how they may affect the driver."
         )}
    ]
    return messages
