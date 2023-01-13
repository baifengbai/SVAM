import configparser
import os
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests,json

class ding_robot:
    def __init__(self):
        self.config = configparser.RawConfigParser()
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        self.config.read(os.path.join(parent_dir,'conf/Ding.ini'))
        robots = eval(self.config.get('common','names'))
        robot_dict = {'sample_robot':{'access_token':'123','secret':'112233'}}
        for robot in robots:
            robot_dict[robot]['access_token'] = self.config.get(robot, 'access_token')
            robot_dict[robot]['secret'] = self.config.get(robot, 'secret')
        self.robot_dict = robot_dict


    def get_sign(self, secret):
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote(base64.b64encode(hmac_code))
        return sign

    def push_message(self,robot,message):
        robot_info = self.robot_dict[robot]
        sign = self.get_sign(robot_info['secret'])
        timestamp = str(round(time.time() * 1000))
        headers={'Content-Type': 'application/json'}   #定义数据类型
        webhook = f'https://oapi.dingtalk.com/robot/send?access_token={robot_info["access_token"]}&timestamp='+timestamp+"&sign="+sign
        data = {
            "msgtype": "text",
            "text": {"content": f'{message}'},
            "isAtAll": True}
        res = requests.post(webhook, data=json.dumps(data), headers=headers)  # 发送post请求