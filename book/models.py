from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField
import json

class Book(models.Model):
    id = IntegerField(primary_key=True)
    book_name = CharField(max_length=100,null=True,name='书名')
    author = CharField(max_length=100,null=True,name='作者')
    file_idm = CharField(max_length=100,null=True)
    douban_id = CharField(max_length=115,null=True)
    cover_img_url = CharField(max_length=300,null = True,name='封面链接')
    brief = CharField(max_length=1000,null = True,name='简介')
    epub_download_url = CharField(max_length=300,null=True)
    mobi_download_url = CharField(max_length=300,null=True)
    pdf_download_url = CharField(max_length=300,null=True)
    azw3_download_url = CharField(max_length=300,null=True)
    date = DateTimeField()

    def __str__(self):
        return self.书名

    def toDict(self):
        return {
        "id":self.id,
        "name":self.书名,
        "author":self.作者,
        "file_idm":self.file_idm,
        "douban_id":self.douban_id,
        "cover_img_url":self.封面链接,
        "brief":self.简介,
        "epub_download_url":self.epub_download_url,
        "mobi_download_url":self.mobi_download_url,
        "pdf_download_url":self.pdf_download_url,
        "azw3_download_url":self.azw3_download_url,
        "date":self.date}

    def toJson(self):
        return json.dumps(self.toDict(),ensure_ascii=False)