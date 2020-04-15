from django.http import HttpResponse
from django.shortcuts import render
import time
from django.views.decorators.csrf import csrf_exempt
from book.models import Book
from django.http import Http404
import requests
import json
import re
from pprint import pprint
import logging
import Levenshtein


logging.basicConfig(format = '%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO,filename='book_net.log')

#从豆瓣获取图书信息
def get_book_data(book_name):
    try:
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.45'}
        #url = 'https://douban.uieee.com/v2/book/search'
        url = 'https://api.douban.com/v2/book/search'
        data_pack = {'q':book_name,'count': 1,'start':0,'apikey':'0b2bdeda43b5688921839c8ecb20399b'}
        data = requests.get(url,headers=headers,params=data_pack)
        if data.status_code != 200:
            return False
        else:
            data = json.loads(data.text)['books']
            if data:
                return data[0]
            else:
                return None
    except:
        return False

#两个字符串的差距
def get_equal_rate(str1, str2):
   return Levenshtein.ratio(str1, str2)

#反爬装饰器
def block_spider(func):
    def _block_spider(*args,**kwargs):
        if "python" in args[0].META["HTTP_USER_AGENT"]:
            h = HttpResponse("400")
            h.status_code = 400
            return h
        else:
            return func(*args, **kwargs)
    return _block_spider

#日志装饰器
def log_record(func):
    def _log_record(*args,**kwargs):
        d = {}
        d['USER_AGENT'] = args[0].META['HTTP_USER_AGENT']
        d['PATH_INFO'] = args[0].META['PATH_INFO']
        d['USER_IP'] = args[0].META['REMOTE_ADDR']
        logging.info(json.dumps(d,ensure_ascii = False))
        return func(*args,**kwargs)
    return _log_record

def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        int(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    
    return False
# Create your views here.
@log_record
@block_spider
def index(request):
    if request.method == "GET":
        a = Book.objects.all()
        total_page = len(a) // 10 + 1
        a = a.order_by('-date')[:10]
    if request.method == "POST":
        search = request.POST.get('search',0)
        if is_number(search):
            a = Book.objects.filter(douban_id = search)
        else:
            if ' ' in search:
                search = search.split(' ')
                a = Book.objects.all()
                for s in search:
                    a = a.filter(book_name__icontains = s)
            else:
                a = Book.objects.filter(book_name__icontains = search)
    return render(request,'book/index.html',{'information':a,'total_page':total_page,'now_page':1})

@log_record
@block_spider
def detail(request,id):
    b = Book.objects.get(douban_id=id)
    print(b)
    return render(request,'book/detail.html',{'information':b})

@log_record
@block_spider
def about(request):
    return render(request,'book/about.html')

@log_record
@block_spider
def page(request,page_num):
    total_page = len(Book.objects.all()) //10 +1
    a = Book.objects.all().order_by('-date')[(page_num-1)*10:page_num*10]
    return render(request,'book/index.html',{'information':a,'total_page':total_page,'now_page':page_num})

@csrf_exempt
def postbox(request):
    if request.method == "POST":
        onedrive_data = json.loads(request.body)
        pprint(onedrive_data)
        file_name_l = onedrive_data['name'].split('.')
        file_name,file_format = file_name_l[0],file_name_l[1]     #将书名和文件格式分离
        douban_data = get_book_data(file_name)
        pprint(douban_data)
        if douban_data == False:
            logging.error('豆瓣api错误')
            h = HttpResponse('豆瓣api错误')
            h.status_code = 417
            return h
        if douban_data == None:
            logging.error('找不到这本书：' + file_name)
            b = Book(book_name = file_name,file_idm=onedrive_data['idm'])
            if file_format == 'epub':
                b.epub_download_url = onedrive_data['url']
                b.epub_flag = True
            if file_format == 'azw3':
                b.azw3_download_url = onedrive_data['url']
                b.azw3_flag = True
            if file_format == 'pdf':
                b.pdf_download_url = onedrive_data['url']
                b.pdf_flag = True
            if file_format == 'mobi':
                b.mobi_download_url = onedrive_data['url']
                b.mobi_flag = True
            b.cover_img_url = 'http://18.222.57.174/book/static/None_cover.png'
            b.douban_id = file_name
            h = HttpResponse('找不到这本书')
            h.status_code = 417
            return h
        if Book.objects.filter(douban_id=douban_data['id']):    #用豆瓣id查询数据库
            b = Book.objects.get(douban_id=douban_data['id'])
            if file_format == 'epub' and b.epub_flag == False:
                b.epub_download_url = onedrive_data['url']
            if file_format == 'azw3' and b.azw3_flag == False:
                b.azw3_download_url = onedrive_data['url']
            if file_format == 'pdf' and b.pdf_flag:
                b.pdf_download_url = onedrive_data['url']
            if file_format == 'mobi' and b.mobi_flag == False:
                b.mobi_download_url = onedrive_data['url']
        else:
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            b = Book(book_name = douban_data['title'],
                     author = douban_data['author'][0],
                 file_idm=onedrive_data['idm'],
                 douban_id=douban_data['id'],
                 cover_img_url='https://images.weserv.nl/?url=' + douban_data['images']['small'][8:],
                 date=date)
            if file_format == 'epub':
                b.epub_download_url = onedrive_data['url']
                b.epub_flag = True
            if file_format == 'azw3':
                b.azw3_download_url = onedrive_data['url']
                b.azw3_flag = True
            if file_format == 'pdf':
                b.pdf_download_url = onedrive_data['url']
                b.pdf_flag = True
            if file_format == 'mobi':
                b.mobi_download_url = onedrive_data['url']
                b.mobi_flag = True
        b.save()
    return HttpResponse('<h1>404</h1>')


def page_not_found(request, exception):
    return render(request,'book/404.html',status=404)
