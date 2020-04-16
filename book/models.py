from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField, BooleanField,TextField
import json

class Book(models.Model):
    id = IntegerField(primary_key=True)
    book_name = CharField(max_length=100,null=True,blank=True,verbose_name='书名')
    author = CharField(max_length=100,null=True,blank=True,verbose_name='作者')
    file_idm = CharField(max_length=200,null=True,blank=True)
    douban_id = CharField(max_length=115,null=True,blank=True)
    cover_img_url = CharField(max_length=300,null = True,verbose_name='封面链接')
    cover_img_large_url = CharField(max_length=300,null = True,blank=True,verbose_name='封面大图链接')
    brief = TextField(default="暂无",null = True,verbose_name='简介')
    epub_download_url = TextField(null=True,blank=True)
    mobi_download_url = TextField(null=True,blank=True)
    pdf_download_url = TextField(null=True,blank=True)
    azw3_download_url = TextField(null=True,blank=True)
    epub_flag = BooleanField(default=False)
    mobi_flag = BooleanField(default=False)
    pdf_flag = BooleanField(default=False)
    azw3_flag = BooleanField(default=False)
    date = DateTimeField()

    def __str__(self):
        return self.book_name

    def saveUrl(self,file_format, url):
        if file_format == 'epub' and self.epub_flag == False:
            self.epub_download_url = url
            self.epub_flag = True
        if file_format == 'azw3' and self.azw3_flag == False:
            self.azw3_download_url = url
            self.azw3_flag = True
        if file_format == 'mobi' and self.mobi_flag == False:
            self.mobi_download_url = url
            self.mobi_flag = True
        if file_format == 'pdf' and self.pdf_flag == False:
            self.pdf_download_url = url
            self.pdf_flag = True

    def toDict(self):
        return {
        "id":self.id,
        "name":self.book_name,
        "author":self.author,
        "file_idm":self.file_idm,
        "douban_id":self.douban_id,
        "cover_img_url":self.cover_img_url,
        "cover_img_large_url":self.cover_img_large_url,
        "brief":self.brief,
        "epub_download_url":self.epub_download_url,
        "mobi_download_url":self.mobi_download_url,
        "pdf_download_url":self.pdf_download_url,
        "azw3_download_url":self.azw3_download_url,
        "date":self.date}

    def toJson(self):
        return json.dumps(self.toDict(),ensure_ascii=False)