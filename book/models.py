from django.db import models
from django.db.models import CharField, DateTimeField, IntegerField, BooleanField, TextField, ForeignKey, FloatField,ManyToManyField
import json

class Book(models.Model):
    file_name = CharField(max_length=100,null=True,blank=True,verbose_name='文件名')
    title = CharField(max_length=100,null=True,blank=True,verbose_name='书名')
    subtitle = CharField(max_length=100,null=True,blank=True,default = '',verbose_name='副标题')
    english_title = CharField(max_length=200,null=True,blank=True,default = '',verbose_name='英文书名')
    author = ManyToManyField('Author',blank=True,related_name='book_author',verbose_name='作者')
    price = CharField(max_length=10,null=True,blank=True,default = '未知',verbose_name='售价')
    cover = CharField(max_length=200,blank=True,default = 'http://18.222.57.174/static/book/images/None_cover.png',verbose_name='封面链接')
    large_cover = CharField(max_length=200,default = 'http://18.222.57.174/static/book/images/None_cover.png',verbose_name='封面大图')
    summary = TextField(null=True,blank=True,default = '暂无',verbose_name='简介')
    catalog = TextField(null=True,blank=True,default = '暂无',verbose_name='目录')
    publisher = ManyToManyField('Publisher',blank=True,related_name='book_publisher',verbose_name='出版社')
    douban_id = CharField(max_length=30,null=True,blank=True,default = '',verbose_name='豆瓣ID')
    true_douban_id = CharField(max_length=30,null=True,blank=True,default = '',verbose_name='用于勘误的豆瓣ID')
    isbn10 = CharField(max_length=20,default = '',null=True,blank=True)
    isbn13 = CharField(max_length=26,default = '',null=True,blank=True)
    pages = CharField(max_length=10,default = '',null=True,blank=True,verbose_name='页数')
    tags = ManyToManyField('Tag',blank=True,related_name='book_tags',verbose_name='标签')
    series = ManyToManyField('Series',blank=True,related_name='book_series',verbose_name='系列')
    translator = ManyToManyField('Translator',blank=True,related_name='book_translator',verbose_name='译者')
    epub_flag = BooleanField(default = False)
    azw3_flag = BooleanField(default = False)
    mobi_flag = BooleanField(default = False)
    pdf_flag = BooleanField(default = False)
    kfx_flag = BooleanField(default = False)
    epub_download = TextField(null=True,blank=True,default = '',verbose_name='EPUB下载链接')
    azw3_download = TextField(null=True,blank=True,default = '',verbose_name='AZW3下载链接')
    mobi_download = TextField(null=True,blank=True,default = '',verbose_name='MOBI下载链接')
    pdf_download = TextField(null=True,blank=True,default = '',verbose_name='PDF下载链接')
    kfx_download = TextField(null=True,blank=True,default = '',verbose_name='KFX下载链接')
    epub_file_size=IntegerField(null=True,blank=True,verbose_name='EPUB文件大小（字节）')
    azw3_file_size=IntegerField(null=True,blank=True,verbose_name='AZW3文件大小（字节）')
    mobi_file_size=IntegerField(null=True,blank=True,verbose_name='MOBI文件大小（字节）')
    pdf_file_size=IntegerField(null=True,blank=True,verbose_name='PDF文件大小（字节）')
    kfx_file_size=IntegerField(null=True,blank=True,verbose_name='KFX文件大小（字节）')
    date = DateTimeField(null=True)

    class Meta:
        verbose_name = "书籍"
        verbose_name_plural = "书籍"

    def save_url(self,url,format,size):
        if format == 'epub' and self.epub_flag == False:
            self.epub_download = url + '?download=1'
            self.epub_flag = True
            self.epub_file_size = int(size)
        if format == 'azw3' and self.azw3_flag == False:
            self.azw3_download = url + '?download=1'
            self.azw3_flag = True
            self.azw3_file_size = int(size)
        if format == 'mobi' and self.mobi_flag == False:
            self.mobi_download = url + '?download=1'
            self.mobi_flag = True
            self.mobi_file_size = int(size)
        if format == 'pdf' and self.pdf_flag == False:
            self.pdf_download = url + '?download=1'
            self.pdf_flag = True
            self.pdf_file_size = int(size)
        if format == 'kfx' and self.kfx_flag == False:
            self.kfx_download = url + '?download=1'
            self.kfx_flag = True
            self.kfx_file_size = int(size)

    def __str__(self):
        if self.subtitle:
            return self.title + ':' + self.subtitle
        else:
            return self.title


class Author(models.Model):
    name = CharField(max_length=30,default = '不详',verbose_name='作者姓名')
    information = TextField(default = '暂无',verbose_name='作者介绍')
    book = ManyToManyField(Book,blank=True,related_name='author_book',verbose_name='作者的书')
    class Meta:
        verbose_name = "作者"
        verbose_name_plural = "作者"

    def __str__(self):
        return self.name

class Series(models.Model):
    name = CharField(max_length=50,verbose_name='系列名')
    book = ManyToManyField(Book,blank=True,related_name='series_book',verbose_name='系列的书')
    class Meta:
        verbose_name = "系列"
        verbose_name_plural = "系列"
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = CharField(max_length=30,verbose_name='标签名')
    title = CharField(max_length=30,verbose_name='标签标题')
    book = ManyToManyField(Book,blank=True,related_name='tag_book',verbose_name='类型的书')
    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
    def __str__(self):
        return self.name

class Translator(models.Model):
    name = CharField(max_length=30,verbose_name='译者姓名')
    book = ManyToManyField(Book,blank=True,related_name='translator_book',verbose_name='译者的书')
    class Meta:
        verbose_name = "译者"
        verbose_name_plural = "译者"
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = CharField(max_length=30,verbose_name='出版社名')
    book = ManyToManyField(Book,blank=True,related_name='publisher_book',verbose_name='出版社的书')
    class Meta:
        verbose_name = "出版社"
        verbose_name_plural = "出版社"
    def __str__(self):
        return self.name

#ManyToManyField('Tag',null=True,blank=True,related_name='',)

#class Book(models.Model):
#    id = IntegerField(primary_key=True,blank=True)
#    book_name = CharField(max_length=100,null=True,blank=True,verbose_name='书名')
#    author = CharField(max_length=100,null=True,blank=True,verbose_name='作者')
#    file_idm = CharField(max_length=200,null=True,blank=True)
#    douban_id = CharField(max_length=115,null=True,blank=True)
#    cover_img_url = CharField(max_length=300,null = True,verbose_name='封面链接')
#    cover_img_large_url = CharField(max_length=300,null = True,blank=True,verbose_name='封面大图链接')
#    brief = TextField(default="暂无",null = True,verbose_name='简介')
#    epub_download_url = TextField(null=True,blank=True)
#    mobi_download_url = TextField(null=True,blank=True)
#    pdf_download_url = TextField(null=True,blank=True)
#    azw3_download_url = TextField(null=True,blank=True)
#    epub_flag = BooleanField(default=False)
#    mobi_flag = BooleanField(default=False)
#    pdf_flag = BooleanField(default=False)
#    azw3_flag = BooleanField(default=False)
#    date = DateTimeField()

#    def __str__(self):
#        return self.book_name

#    def saveUrl(self,file_format, url):
#        if file_format == 'epub' and self.epub_flag == False:
#            self.epub_download_url = url
#            self.epub_flag = True
#        if file_format == 'azw3' and self.azw3_flag == False:
#            self.azw3_download_url = url
#            self.azw3_flag = True
#        if file_format == 'mobi' and self.mobi_flag == False:
#            self.mobi_download_url = url
#            self.mobi_flag = True
#        if file_format == 'pdf' and self.pdf_flag == False:
#            self.pdf_download_url = url
#            self.pdf_flag = True

#    def toDict(self):
#        return {
#        "id":self.id,
#        "name":self.book_name,
#        "author":self.author,
#        "file_idm":self.file_idm,
#        "douban_id":self.douban_id,
#        "cover_img_url":self.cover_img_url,
#        "cover_img_large_url":self.cover_img_large_url,
#        "brief":self.brief,
#        "epub_download_url":self.epub_download_url,
#        "mobi_download_url":self.mobi_download_url,
#        "pdf_download_url":self.pdf_download_url,
#        "azw3_download_url":self.azw3_download_url,
#        "date":self.date}

#    def toJson(self):
#        return json.dumps(self.toDict(),ensure_ascii=False)

