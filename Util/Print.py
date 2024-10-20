# color_print_utils.py

class ColorPrint:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def red(text):
        return f"{ColorPrint.RED}{text}{ColorPrint.END}"

    @staticmethod
    def green(text):
        return f"{ColorPrint.GREEN}{text}{ColorPrint.END}"

    @staticmethod
    def blue(text):
        return f"{ColorPrint.BLUE}{text}{ColorPrint.END}"

    @staticmethod
    def bold(text):
        return f"{ColorPrint.BOLD}{text}{ColorPrint.END}"

    @staticmethod
    def underline(text):
        return f"{ColorPrint.UNDERLINE}{text}{ColorPrint.END}"

    @staticmethod
    def yellow(text):
        return f"{ColorPrint.YELLOW}{text}{ColorPrint.END}"

    @staticmethod
    def cyan(text):
        return f"{ColorPrint.CYAN}{text}{ColorPrint.END}"