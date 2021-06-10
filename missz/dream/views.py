# Create your views here.
from django.http import HttpResponse, JsonResponse

from . import tasks, db, utils
from .gen_image import gen_image
# import asyncio
# import _thread

import urllib.request
import json
import logging
import re


def all_dream(request):
    return db.get_all_db()


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


def delBadSentence(txt):
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
        if len(line) <= 4:
            continue
        if line[-1] == ':' or line[-1] == '：':
            continue
        list_1.append(line)
    return_string = ""
    for str in list_1:
        return_string += str
        if return_string[-1] == '。' and len(return_string) >= 200:
            return return_string
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

    if db.ask_db(dream):
        # print("same dream")
        interpret, _, _, _ = db.get_db(dream)
        # print("return ", interpret)
        return JsonResponse({'interpret': interpret})

    # content = "身份：军人。年龄：25岁。性别：女。梦境：" + dream + "周公解梦：这个梦的含义是，"
    content = dream + " 周公解梦：这个梦的含义是,"
    body = {
        "token": utils.TOKEN,
        "app": "chat",
        "content": content
    }
    print("content:" + content)
    # print("content len: "+len(content))
    # print("content len: " + str(len(content)))
    data = bytes(json.dumps(body), 'utf8')
    headers = {"Content-Type": 'application/json'}
    req = urllib.request.Request(url=utils.URL_GPT, headers=headers, data=data)

    # 同时多次请求
    # try:
    #     _thread.start_new_thread(tasks.ask_for_interpret_competely, (dream,body, ))
    # except Exception as e:
    #     print("Error: unable to start thread", e)

    try:
        resp = urllib.request.urlopen(req).read()
        print("主线程收到解梦\n")
        print(resp.decode('utf-8'))
    except Exception as e:
        logging.error(e)
        print(e)
    try:
        res = json.loads(resp).get("result")
        deduplication_txt = deduplication(res)
        interpret = deduplication_txt[deduplication_txt.find("这个梦的含义是") + 8:]
        interpret = delBadSentence(interpret)
        if interpret == "":
            return HttpResponse("此梦境前无古人后无来者，简直太厉害了。")
        db.insert_db(dream, interpret, utils.embed2str(utils.get_embedding(dream)), 0, 0)
        # get_db(dream)
        return JsonResponse({'interpret': interpret})
    except Exception as e:
        logging.error(e)
        print("error happened!")
        return HttpResponse("error happened!")


def similar_dream(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            dream = req.get('dream')
        except Exception as e:
            print(e)
    else:
        return_json = 'POST only!'
        return HttpResponse(return_json)
    embedding = utils.get_embedding(dream)

    json_data = {"data": utils.get_similar_dream(embedding)}
    return JsonResponse(json_data, status=200)


def check_times(request):
    body = {
        "token": utils.TOKEN
    }
    data = json.dumps(body)
    data = bytes(data, 'utf8')
    print(data)
    headers = {"Content-Type": 'application/json'}
    req = urllib.request.Request(url=utils.URL_USER, headers=headers, data=data)
    try:
        resp = urllib.request.urlopen(req).read()
        print(resp.decode('utf-8'))
    except Exception as e:
        logging.error(e)
        print(e)
    return HttpResponse(resp)


def get_good(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            dream = req.get('dream')
            if db.ask_db(dream):
                interpret, embed, good, bad = db.get_db(dream)
                good += 1
                db.insert_db(dream, interpret, embed, good, bad)
                return HttpResponse(good)
            else:
                return_json = 'dream not exist!'
                return HttpResponse(return_json)
        except Exception as e:
            print(e)
    else:
        return_json = 'POST only!'
        return HttpResponse(return_json)


def get_bad(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            dream = req.get('dream')
            if db.ask_db(dream):
                interpret, embed, good, bad = db.get_db(dream)
                bad += 1
                db.insert_db(dream, interpret, embed, good, bad)
                return HttpResponse(bad)
            else:
                return_json = 'dream not exist!'
                return HttpResponse(return_json)
        except Exception as e:
            print(e)
    else:
        return_json = 'POST only!'
        return HttpResponse(return_json)


def get_image(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            dream = req.get('dream')
            print(f'get dream {dream}')
            if db.ask_db(dream):
                interpret, embed_, good_, bad_ = db.get_db(dream)
                code = hash(dream)
                gen_image(code, dream, interpret)
                return JsonResponse({'src': f'/backend/dream/media/{code}.png'})
            else:
                return_json = 'dream not exist!'
                return HttpResponse(return_json)
        except Exception as e:
            print(e)
    else:
        return_json = 'POST only!'
        return HttpResponse(return_json)
