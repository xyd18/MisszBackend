# Create your views here.
from django.http import HttpResponse
import urllib.request
import json
import logging

TOKEN = "c486e142f0ed6050f8d0497968079eb2"
TOKEN_PUB = "da5d90ab00b50c2ba032d944d75f95db"
URL_USER = "http://lab.aminer.cn/isoa-2021/user"
URL_GPT = "http://lab.aminer.cn/isoa-2021/gpt"

def interpret_dream(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        # name = req.get('name')
        dream = req.get('dream')
        print(dream)
        # return_json = json.dumps((name, job))
        # return HttpResponse(return_json)
    else:
        return_json = 'POST only!'
        return HttpResponse(return_json)
    # content = "身份：军人。年龄：25岁。性别：女。梦境：" + dream + "周公解梦：这个梦的含义是，"
    content = dream + "周公解梦：这个梦的含义是，"
    body = {
        "token": TOKEN,
        "app": "chat",
        "content": content
    }
    data = bytes(json.dumps(body), 'utf8')
    headers = {"Content-Type": 'application/json'}
    req = urllib.request.Request(url=URL_GPT, headers=headers, data=data)
    try:
        resp = urllib.request.urlopen(req).read()
        print(resp.decode('utf-8'))
    except Exception as e:
        logging.error(e)
        print(e)
    res = json.loads(resp)
    interpret = res.get("result")[len(content):]
    return HttpResponse(interpret)

def check_times(request):
    body = {
        "token": TOKEN
    }
    data = json.dumps(body)
    data = bytes(data, 'utf8')
    print(data)
    headers = {"Content-Type": 'application/json'}
    req = urllib.request.Request(url=URL_USER, headers=headers, data=data)
    try:
        resp = urllib.request.urlopen(req).read()
        print(resp.decode('utf-8'))
    except Exception as e:
        logging.error(e)
        print(e)
    return HttpResponse(resp)