from django.db import models

# Create your models here.
class dreamEntry(models.Model):
    id = models.AutoField(primary_key=True)
    dream = models.TextField()
    interpret = models.TextField()
    sentence_embedding = models.JSONField(null=True)
    good_num = models.BigIntegerField(default=0)
    bad_num = models.BigIntegerField(default=0)