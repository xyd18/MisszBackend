import json
import re
import urllib.request
from . import views
TOKEN = "c486e142f0ed6050f8d0497968079eb2"
TOKEN_PUB = "da5d90ab00b50c2ba032d944d75f95db"
URL_USER = "http://lab.aminer.cn/isoa-2021/user"
URL_GPT = "http://lab.aminer.cn/isoa-2021/gpt"

def ask_for_interpret_competely(dream, body):
    """
    body = {
        "token": TOKEN,
        "app": "chat",
        "content": content
    }
    """
    # print("异步多次请求获得解梦存到数据库中")
    headers = {"Content-Type": 'application/json'}

    interpret = "这个梦的含义是,"
    n = 0

    while n < 5 and len(body["content"]) < 100:
        n += 1
        try:
            # print("content: " + body["content"])
            data = bytes(json.dumps(body), 'utf8')
            req = urllib.request.Request(url=URL_GPT, headers=headers, data=data)
            resp = urllib.request.urlopen(req).read()
            print(n,"收到解梦:")
            print(resp.decode('utf-8'))
        except Exception as e:
            print(e)
        try:
            result = json.loads(resp).get("result")
            new_interpret = result[result.find(interpret[:-1])+len(interpret):]
            # print("result[result.find(interpret)+len(interpret):]", new_interpret)

            split_line = re.split(r"([.。!！?？；;：:\s+])", new_interpret)
            split_line.append("")
            split_line = ["".join(i) for i in zip(split_line[0::2], split_line[1::2])]
            i = 0
            new_interpret = split_line[i]
            while new_interpret == r"(\s+)" or new_interpret == "":
                i += 1
                if i >= len(split_line):
                    break
                new_interpret = split_line[i]
            print(n, new_interpret)
            if new_interpret == r"(\s+)" or new_interpret == "" or new_interpret == " ":
                print("no new interpret")
                continue
            else:
                interpret = new_interpret
                body["content"] += interpret
        except Exception as e:
            print("error happened!", e)
    deduplication_txt = views.deduplication(body["content"])
    interpret = deduplication_txt[deduplication_txt.find("这个梦的含义是") + 8:]
    views.insert_db(dream, interpret, "")
    print("insert: ",dream, interpret)
