from sentence_transformers import SentenceTransformer, util
from dream.models import dreamEntry

TOKEN = "c486e142f0ed6050f8d0497968079eb2"
TOKEN_PUB = "da5d90ab00b50c2ba032d944d75f95db"
URL_USER = "http://lab.aminer.cn/isoa-2021/user"
URL_GPT = "http://lab.aminer.cn/isoa-2021/gpt"

def compute_all_embeddings():
	model = SentenceTransformer('paraphrase-TinyBERT-L6-v2')

	for d in dreamEntry.objects.all():
		embedding = model.encode(d.dream)
		

