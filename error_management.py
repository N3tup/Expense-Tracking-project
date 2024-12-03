import sys
import colorama
from colorama import Fore, Style

def handle_error(error_type, error_message):
    print(f"{Fore.RED}An error occurred: {error_type}: {error_message}{Style.RESET_ALL}")
    sys.exit(1)

def file_error(error_message):
    handle_error("File Error", error_message)

def input_error(error_message):
    handle_error("Input Error", error_message)

def date_error(error_message):
    handle_error("Date Error", error_message)

colorama.init()


