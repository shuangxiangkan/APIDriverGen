import os
import warnings
from tree_sitter import Language, Parser


class C_Parser_Builder:
    """Class to build a parser for a specific language."""

    def __init__(self, language):
        self.language = language
        # 获取当前文件的目录
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def build(self):
        build_path = os.path.join(self.current_dir, 'build')
        vendor_path = os.path.join(self.current_dir, 'vendor')

        # 确保 build 和 vendor 目录存在
        os.makedirs(build_path, exist_ok=True)
        os.makedirs(vendor_path, exist_ok=True)

        language_so = os.path.join(build_path, f'{self.language}-languages.so')
        if not os.path.exists(language_so):
            tree_sitter_path = os.path.join(vendor_path, f'tree-sitter-{self.language}')
            if not os.path.exists(tree_sitter_path):
                os.system(f'git clone https://github.com/tree-sitter/tree-sitter-{self.language} {tree_sitter_path}')

            Language.build_library(
                language_so,
                [tree_sitter_path]
            )

        # 使用 warnings.catch_warnings() 来抑制特定的警告
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            LANGUAGE = Language(language_so, self.language)

        parser = Parser()
        parser.set_language(LANGUAGE)
        return parser