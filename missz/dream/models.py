from django.db import models

# Create your models here.
class dreamEntry(models.Model):
    dream = models.TextField(primary_key=True)
    interpret = models.TextField()
    sentence_embedding = models.JSONField(null=True)
    good_num = models.BigIntegerField(default=0)
    bad_num = models.BigIntegerField(default=0)