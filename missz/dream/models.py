from django.db import models

class dreamEntry(models.Model):
    dream = models.TextField(primary_key=True)
    interpret = models.TextField()
    sentence_embedding = models.TextField()
    good_num = models.BigIntegerField(default=0)
    bad_num = models.BigIntegerField(default=0)