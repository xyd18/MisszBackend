from sentence_transformers import SentenceTransformer, util
from dream.models import dreamEntry

TOKEN = "c486e142f0ed6050f8d0497968079eb2"
TOKEN_PUB = "da5d90ab00b50c2ba032d944d75f95db"
URL_USER = "http://lab.aminer.cn/isoa-2021/user"
URL_GPT = "http://lab.aminer.cn/isoa-2021/gpt"



def str2list(string):
	strlist = string.split(",")
	embed = [float(i) for i in strlist]
	return embed

def embed2str(embed):
	strlist = [str(num) for num in embed]
	return ",".join(strlist)

def compute_all_embeddings():
	model = SentenceTransformer('paraphrase-TinyBERT-L6-v2')

	for d in dreamEntry.objects.all():
		embedding = model.encode(d.dream)


def get_similar_dream(dream_embedding):
    # if request.method == 'POST':
    #     try:
    #         req = json.loads(request.body)
    #         dream = req.get('dream')
    #         # print("收到梦境 " + dream)
    #     # return_json = json.dumps((name, job))
    #     # return HttpResponse(return_json)
    #     except Exception as e:
    #         print(e)
    # else:
    #     return_json = 'POST only!'
    #     return HttpResponse(return_json)
    pass
