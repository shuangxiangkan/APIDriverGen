import random
from z3 import *
import tree_sitter
# from tree_sitter import Language, Parser
from Parser.C.C_Parser import C_Parser_Builder

# 模拟大模型生成的fuzz driver
def generate_fuzz_driver():
    driver = """
    #include <stdio.h>
    #include <stdlib.h>

    void target_api(int option);

    int main() {
        int option = rand() % 9 + 1;  // 生成1到9之间的随机数
        target_api(option);
        return 0;
    }
    """
    return driver


# 使用tree-sitter解析C代码
def parse_fuzz_driver(driver_code):
    # Language.build_library(
    #     'build/my-languages.so',
    #     ['vendor/tree-sitter-c']
    # )
    # C_LANGUAGE = Language('build/my-languages.so', 'c')
    # parser = Parser()
    # parser.set_language(C_LANGUAGE)

    parser = C_Parser_Builder('c').build()
    tree = parser.parse(bytes(driver_code, "utf8"))
    return tree


# 提取option的生成逻辑
def extract_option_generation(node):
    if node.type == 'binary_expression' and node.children[1].type == 'modulo':
        left = node.children[0].text.decode('utf8')
        right = node.children[2].text.decode('utf8')
        if left == 'rand()' and right == '9':
            return True
    for child in node.children:
        if extract_option_generation(child):
            return True
    return False


# 使用Z3验证option生成的正确性
def verify_option_generation():
    s = Solver()
    option = Int('option')

    # option应该在1到9之间
    s.add(option >= 1, option <= 9)

    # 验证所有可能的值
    for i in range(1, 10):
        s.push()
        s.add(option == i)
        if s.check() != sat:
            s.pop()
            return False
        s.pop()

    # 验证不可能的值
    s.push()
    s.add(Or(option < 1, option > 9))
    if s.check() == sat:
        s.pop()
        return False
    s.pop()

    return True


# 主函数
def main():
    # 生成fuzz driver
    driver_code = generate_fuzz_driver()
    print("Generated Fuzz Driver:")
    print(driver_code)

    # 解析fuzz driver
    tree = parse_fuzz_driver(driver_code)

    # 提取和验证option生成逻辑
    if extract_option_generation(tree.root_node):
        print("Option generation logic found in the driver.")
        if verify_option_generation():
            print("Z3 verification passed: Option generation is correct.")
        else:
            print("Z3 verification failed: Option generation is incorrect.")
    else:
        print("Option generation logic not found in the driver.")


if __name__ == "__main__":
    main()