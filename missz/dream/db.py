from . import models
from django.http import JsonResponse


def insert_db(dream, interpret, sent_embed, good_num=0, bad_num=0):
    dreams_in_db = models.dreamEntry.objects.filter(dream=dream)
    if dreams_in_db.count() == 0:
        models.dreamEntry.objects.create(dream=dream, interpret=interpret, sentence_embedding=sent_embed, good_num=good_num, bad_num=bad_num)
    else:
        dreams_in_db.update(interpret=interpret, sentence_embedding=sent_embed, good_num=good_num, bad_num=bad_num)


def delete_db(dream):
    models.dreamEntry.object.filter(dream=dream).delete()


def get_db(dream):
    dream_in_db = models.dreamEntry.objects.get(dream=dream)
    return dream_in_db.interpret, dream_in_db.sentence_embedding, dream_in_db.good_num, dream_in_db.bad_num


def ask_db(dream):
    dreams_in_db = models.dreamEntry.objects.filter(dream=dream)
    if dreams_in_db.count() == 0:
        return False
    return True


def get_all_db():
    data_list = models.dreamEntry.objects.all().order_by("good_num")
    info = []
    for data in data_list:
        dream = data.dream
        interpret = data.interpret
        good_num = data.good_num
        bad_num = data.bad_num
        meta_dict = {"dream": dream, "interpret": interpret, "good_num": good_num, "bad_num": bad_num}
        info.append(meta_dict)
    json_data = {"data": info}
    return JsonResponse(json_data, status=200)