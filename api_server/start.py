import json
import os

import requests
from flask import Flask, request, Response
from storage.rabbitmq import rabbit

rabbit.init_queue(['download','douyin_upload','kuaishou_upload'])
app = Flask("my-app")



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/add', methods=['POST'])
def add():
    print(request.headers)
    print(type(request.json))
    print(request.json)
    result = request.json['a'] + request.json['b']
    return str(result)

@app.route('/add2', methods=['POST'])
def add2():
    result = {'sum': request.json['a'] + request.json['b']}
    return Response(json.dumps(result),  mimetype='application/json')

# 视频链接解析
@app.route('/video_link_analysis', methods=['POST'])
def video_link_analysis():
    video_link = request.json['video_link']
    res = requests.get('http://192.168.31.214:22980/?url='+video_link)
    if res.json()['code'] == 200:
        result = {'code':200,'data':res.json()['data']}
        return Response(json.dumps(result), mimetype='application/json')
    else:
        result = {'code':999,'data':{}}
        return Response(json.dumps(result), mimetype='application/json')

# 下载到服务器
@app.route('/download_to_server', methods=['POST'])
def download_to_server():
    download_url = request.json['url']
    file_name = request.json['file_name']
    save_path = request.json['save_path']
    rabbit.insert_message_into_queue('download',request.json)
    return 'ok'

# 上传到服务器
@app.route('/upload_to_server', methods=['POST'])
def upload_to_server():
    bytes = request.json['bytes']
    file_name = request.json['file_name']
    save_path = request.json['save_path']
    file_write = open(os.path.join(save_path, file_name), "wb")
    file_write.write(bytes)
    file_write.close()
    return 'ok'

# 获取待发布视频
@app.route('/get_up_video', methods=['POST'])
def get_up_video():
    platform = request.json['platform']
    type = request.json['type']
    queue_name= platform+f'_{type}'+'_upload'
    message=rabbit.get_message(queue_name)
    return message

# 记录日志
@app.route('/logger', methods=['POST'])
def logger():
    module = request.json['module']
    level = request.json['level']


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=21000, debug=True)
