import json
import os

import requests
from flask import Flask, request, Response

from storage.rabbitmq import rabbit

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models

# rabbit.init_queue(['download','douyin_upload','kuaishou_upload'])
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

# 人脸识别
@app.route("/face", methods=['POST'])
def face():
    try:
        if not request.json['url']:
            image_64 = request.json['image']
            image_url = ""
            params = {
                "Image": image_64,
                "NeedFaceAttributes": 1
            }
        else:
            image_url = request.json['url']
            image_64 = ""
            params = {
                "Url": image_url,
                "NeedFaceAttributes": 1
            }
        if not (image_64 or image_url):
            result = {'code':201,'data':"没有图片！"}
            return Response(json.dumps(result), mimetype='application/json')
        cred = credential.Credential("AKIDCDyTheKp30g4C3ez4sPffOq1vZv0oMdd", "lGUR7WeV5ORDivta0bw1pMbaHistd6ID")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "iai.tencentcloudapi.com"
        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = iai_client.IaiClient(cred, "ap-shanghai", clientProfile)
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DetectFaceRequest()
        req.from_json_string(json.dumps(params))
        # 返回的resp是一个DetectFaceResponse的实例，与请求对象对应
        resp = client.DetectFace(req)
        # 输出json格式的字符串回包
        res = json.loads(resp.to_json_string())
        res = res['FaceInfos'][0]
        print(res)
        result = {'code':200,'data':json.dumps(res)}
        return Response(json.dumps(result), mimetype='application/json')
    except:
        result = {'code':202,'data':''}
        return Response(json.dumps(result), mimetype='application/json')
# 视频链接解析
@app.route('/video_link_analysis', methods=['POST'])
def video_link_analysis():
    video_link = request.json['video_link']
    print(video_link)
    video_link = 'http'+video_link.split('http')[-1]
    print(video_link)
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
    app.run(host='0.0.0.0', port=21000)
