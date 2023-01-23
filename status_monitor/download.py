from pathlib import Path
from time import sleep

import requests


from api_server.storage.rabbitmq import rabbit


def download_file():
    while True:
        data = rabbit.get_message('download')
        if data:
            data = data['data']
            if data['url'] == '0':
                continue
            response = requests.get(data['url'])
            if response.status_code != 200:
                raise ValueError("下载文件网站返回码异常，请检查后重试")
            f = open(Path.joinpath(data['save_path'],data['file_name']),'wb')
            f.write(response.content)
            f.close()
        else:
            sleep(10)
