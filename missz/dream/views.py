# Create your views here.
from django.http import HttpResponse
from . import models
import urllib.request
import json
import logging
import re

TOKEN = "c486e142f0ed6050f8d0497968079eb2"
TOKEN_PUB = "da5d90ab00b50c2ba032d944d75f95db"
URL_USER = "http://lab.aminer.cn/isoa-2021/user"
URL_GPT = "http://lab.aminer.cn/isoa-2021/gpt"


def insert_db(dream, interpret, sent_embed):
    dreams_in_db = models.dreamEntry.objects.filter(dream=dream)
    if dreams_in_db.count() == 0:
        models.dreamEntry.objects.create(dream=dream, interpret=interpret, sentence_embedding=sent_embed)
    else:
        dreams_in_db.update(interpret=interpret)


def delete_db(dream):
    models.dreamEntry.object.filter(dream=dream).delete()


def get_db(dream):
    dream_in_db = models.dreamEntry.objects.get(dream=dream)
    return dream_in_db.interpret

def ask_db(dream):
    dreams_in_db = models.dreamEntry.objects.filter(dream=dream)
    if dreams_in_db.count() == 0:
        return False
    return True

def deduplication(txt):
    lines = re.split(r"([.。!！?？；;：:，,\s+])", txt)
    # for line in lines:
    #     print(line+"\n")
    # print("\n\n")
    lines.append("")
    lines = ["".join(i) for i in zip(lines[0::2], lines[1::2])]
    # for line in lines:
    #     print(line+"\n")
    list_1 = []
    for line in lines:
        if len(line) <= 1:
            continue
        if line[0:-1] not in list_1:
            list_1.append(line[0:-1])
            list_1.append(line[-1])
    return_string = ""
    for str in list_1:
        return_string += str
    return return_string


def interpret_dream(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            # name = req.get('name')
            dream = req.get('dream')
            print("收到梦境 " + dream)
        # return_json = json.dumps((name, job))
        # return HttpResponse(return_json)
        except Exception as e:
            print(e)
    else:
        return_json = 'POST only!'
        print(return_json)
        return HttpResponse(return_json)

    if ask_db(dream):
        return HttpResponse(get_db(dream))

    # content = "身份：军人。年龄：25岁。性别：女。梦境：" + dream + "周公解梦：这个梦的含义是，"
    content = dream + " 周公解梦：这个梦的含义是，"
    body = {
        "token": TOKEN,
        "app": "chat",
        "content": content
    }
    print("content:" + content)
    print("content len: " + str(len(content)))
    data = bytes(json.dumps(body), 'utf8')
    headers = {"Content-Type": 'application/json'}
    req = urllib.request.Request(url=URL_GPT, headers=headers, data=data)

    try:
        resp = urllib.request.urlopen(req).read()
        print("收到解梦\n")
        print(resp.decode('utf-8'))
    except Exception as e:
        logging.error(e)
        print(e)
    try:
        res = json.loads(resp)
        deduplication_txt = deduplication(res.get("result"))
        interpret = deduplication_txt[deduplication_txt.find("这个梦的含义是") + 8:]
        insert_db(dream, interpret, "")
        # get_db(dream)
        return HttpResponse(interpret)
    except Exception as e:
        logging.error(e)
        return HttpResponse("error happened!")


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
