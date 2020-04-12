from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField
import json

class Book(models.Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100,null=True)
    author = CharField(max_length=100,null=True)
    file_idm = CharField(max_length=100,null=True)
    douban_id = CharField(max_length=115,null=True)
    cover_img_url = CharField(max_length=300,null = True)
    brief = CharField(max_length=1000,null = True)
    epub_download_url = CharField(max_length=300,null=True)
    mobi_download_url = CharField(max_length=300,null=True)
    pdf_download_url = CharField(max_length=300,null=True)
    azw3_download_url = CharField(max_length=300,null=True)
    date = DateTimeField()

    def __str__(self):
        return self.name

    def toDict(self):
        return {
        "id":self.id,
        "name":self.name,
        "author":self.author,
        "file_idm":self.file_idm,
        "douban_id":self.douban_id,
        "cover_img_url":self.cover_img_url,
        "brief":self.brief,
        "epub_download_url":self.epub_download_url,
        "mobi_download_url":self.mobi_download_url,
        "pdf_download_url":self.pdf_download_url,
        "azw3_download_url":self.azw3_download_url,
        "date":self.date}
    def toJson(self):
        return json.dumps(self.toDict(),ensure_ascii=False)