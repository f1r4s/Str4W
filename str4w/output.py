from colorama import Fore


def print_error(*args, sep=' ', end='\n', file=None):
    print(f"[{Fore.RED}!!{Fore.RESET}]", *args, sep=sep, end=end, file=file)


def print_warning(*args, sep=' ', end='\n', file=None):
    print(f"[{Fore.YELLOW}!{Fore.RESET}]", *args, sep=sep, end=end, file=file)


def print_success(*args, sep=' ', end='\n', file=None):
    print(f"[{Fore.GREEN}+{Fore.RESET}]", *args, sep=sep, end=end, file=file)


def print_info(*args, sep=' ', end='\n', file=None):
    print(f"[{Fore.CYAN}*{Fore.RESET}]", *args, sep=sep, end=end, file=file)


def ask_yn(question):
    print(f"[{Fore.YELLOW}?{Fore.RESET}]", question, end="")
    return input().upper() == 'Y'
