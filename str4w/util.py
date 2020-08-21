import re
import string
import random

from colorama import Fore


def verify_url(url: str) -> bool:
    return re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)


def random_string(length: int, characters: list = string.ascii_letters):
    return ''.join([random.choice(characters) for _ in range(length)])


def random_color():
    colors = [Fore.YELLOW, Fore.MAGENTA, Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.RED, Fore.WHITE]
    return random.choice(colors)


def sum_dicts(accumulator, element):
    for key, value in element.items():
        accumulator[key] = accumulator.get(key, 0) + value
    return accumulator
