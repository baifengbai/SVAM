import json

import requests
from flask import Flask, request, Response
from storage.rabbitmq import Mq

rabbit = Mq()
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
