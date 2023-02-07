import requests
from environs import Env


def create_file(file_path, message):
    env = Env()
    env.read_env(r'env')
    API = env('BOT_TOKEN')
    API = f'https://api.telegram.org/bot{API}/sendDocument'
    f = open(file_path, 'rb')
    file_bytes = f.read()
    f. close()
    files = {'document': (f.name, file_bytes)}
    parameters = {'chat_id': message}
    r = requests.post(url=API, data=parameters, files=files)
    return r.status_code
