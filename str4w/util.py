import re
import string
import random


def verify_url(url: str) -> bool:
    return re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)


def random_string(length: int, characters: list = string.ascii_letters):
    return ''.join([random.choice(characters) for _ in range(length)])
