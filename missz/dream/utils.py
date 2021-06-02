from sentence_transformers import SentenceTransformer, util
from dream.models import dreamEntry
from dream.db import insert_db


TOKEN = "c486e142f0ed6050f8d0497968079eb2"
TOKEN_PUB = "da5d90ab00b50c2ba032d944d75f95db"
URL_USER = "http://lab.aminer.cn/isoa-2021/user"
URL_GPT = "http://lab.aminer.cn/isoa-2021/gpt"

model = SentenceTransformer('paraphrase-TinyBERT-L6-v2')

def str2list(string):
    strlist = string.split(",")
    embed = [float(i) for i in strlist]
    return embed

def embed2str(embed):
    strlist = [str(num) for num in embed]
    return ",".join(strlist)

def compute_all_embeddings():
    for d in dreamEntry.objects.all():
        embedding = model.encode(d.dream)
        insert_db(d.dream, d.interpret, embed2str(embedding), d.good_num, d.bad_num)

def get_embedding(dream_str):
    return model.encode(dream_str)

def get_similar_dream(dream_embedding):

    res = []

    data_list = dreamEntry.objects.all()
    for data in data_list:
        dream = data.dream
        interpret = data.interpret
        good_num = data.good_num
        bad_num = data.bad_num
        emb = str2list(data.sentence_embedding)
        cos_sim = float(util.pytorch_cos_sim(dream_embedding, emb))
        meta_dict = {"dream": dream, "interpret": interpret, "good_num": good_num, "bad_num": bad_num, "cos_sim":cos_sim}
        res.append(meta_dict)

    def takeSim(elem):
        return elem["cos_sim"]

    res.sort(key=takeSim, reverse=True)

    return res
