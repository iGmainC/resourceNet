from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField
import json

class Book(models.Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100,null=True)
    author = CharField(max_length=100)
    file_idm = CharField(max_length=100,null=True)
    douban_id = CharField(max_length=115,null=True)
    epub_download_url = CharField(max_length=300,null=True)
    mobi_download_url = CharField(max_length=300,null=True)
    pdf_download_url = CharField(max_length=300,null=True)
    azw3_download_url = CharField(max_length=300,null=True)
    cover_img_url = CharField(max_length=300,null = True)
    date = DateTimeField()

    def __str__(self):
        return self.name