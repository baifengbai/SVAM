from pathlib import Path
from time import sleep

import requests

from api_server.storage.rabbitmq import rabbit
from api_server.storage.mysql import mysql


def download_file():
    while True:
        data = rabbit.get_message_not_ack('download')
        if data:
            data = data['data']
            if data['url'] == '0':
                continue
            response = requests.get(data['url'])
            if response.status_code != 200:
                continue
            rabbit.ack_this_message()
            f = open(Path.joinpath(data['save_path'], data['file_name']), 'wb')
            f.write(response.content)
            f.close()
            data_type = mysql.get_data_from_mysql('source_info', 'data_type', f"uuid='{data['uuid']}'")
            if data_type == '抖音':
                if '.mp4' in data['file_name']:
                    mysql.update_data_into_mysql('source_info',
                                                 f"main_file='{Path.joinpath(data['save_path'], data['file_name'])}'",
                                                 f"uuid='{data['uuid']}'")
                else:
                    mysql.update_data_into_mysql('source_info',
                                                 f"link_1='{Path.joinpath(data['save_path'], data['file_name'])}'",
                                                 f"uuid='{data['uuid']}'")
        else:
            sleep(10)
