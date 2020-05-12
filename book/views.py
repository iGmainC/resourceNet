from django.http import HttpResponse
from django.shortcuts import render
import time
from django.views.decorators.csrf import csrf_exempt
from book.models import Book,Author,Series,Tag,Translator,Publisher
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

#推送
def push_book(file_name,mail):
    url = 'https://prod-04.southeastasia.logic.azure.com:443/workflows/53a4063f223544789f407e0d8b1a23af/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=psQUXlsBA7zbp64EY4Hw0HpLhddnBhmOD5a7ROxwwY8'
    headers = {'Content-Type': 'application/json'}
    d = {}
    d["file_name"] = file_name
    d['mail']=mail
    r = requests.post(url,headers=headers,data=json.dumps(d),timeout=200)
    print([r.status_code,r.text])
    return [r.status_code,r.text]

#反爬装饰器
def block_spider(func):
    def _block_spider(*args,**kwargs):
        if args[0].META["HTTP_USER_AGENT"]:
            if "python" in args[0].META["HTTP_USER_AGENT"]:
                h = HttpResponse("400")
                h.status_code = 400
                return h
            else:
                return func(*args, **kwargs)
        else:
            h = HttpResponse("400")
            h.status_code = 400
            return h
    return _block_spider

#日志装饰器
def log_record(func):
    def _log_record(*args,**kwargs):
        d = {}
        d['USER_AGENT'] = args[0].META['HTTP_USER_AGENT']
        d['PATH_INFO'] = args[0].META['PATH_INFO']
        http_forwarded_for = args[0].META.get('HTTP_X_FORWARDED_FOR')
        d['REMOTE_HOST'] = args[0].META.get('REMOTE_HOST')
        if http_forwarded_for:
            d['USER_IP'] = http_forwarded_for.split(',')[0]
        else:
            d['USER_IP'] = args[0].META['REMOTE_ADDR']
        logging.info(str(json.dumps(d,ensure_ascii = False)) + '\n')
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
    total_page = len(Book.objects.all()) // 10 + 1
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
                    a = a.filter(title__icontains = s)
            else:
                a = Book.objects.filter(title__icontains = search)
            total_page = len(a) // 10 + 1
    return render(request,'book/index.html',{'information':a,'total_page':total_page,'now_page':1})

@log_record
@block_spider
def detail(request,id):
    is_n_flag = is_number(id)
    if is_n_flag:
        b = Book.objects.filter(douban_id=id)
    else:
        b = Book.objects.filter(file_name=id)
    if b:
        if is_n_flag:
            b = Book.objects.get(douban_id=id)
        else:
            b = Book.objects.get(file_name=id)
        return render(request,'book/detail.html',{'information':b})
    return render(request,'book/404.html',status = 404)

@log_record
@block_spider
def about(request):
    return render(request,'book/about.html')

@csrf_exempt
def push(request):
    mail = request.POST.get('mail')
    file_name = request.POST.get('file_name')
    state = push_book(file_name+'.mobi',mail)
    if state[0] == 200:
        return render(request,'book/push.html',{'state':'成功！','inf':''})
    if state[0]==404:
        b = Book.objects.get(file_name=file_name)
        b.mobi_file_size=int(state[1])
        b.save()
        return render(request,'book/push.html',{'state':'失败！','inf':'文件过大，为 '+str(int(state[1])/1024//1024)+'MB 限制为25MB'})
    else:
        return render(request,'book/push.html',{'state':'失败！','inf':'未知错误，请重试'})
    return render(request,'book/404.html',status = 404)


@log_record
@block_spider
def page(request,page_num):
    total_page = len(Book.objects.all()) // 10 + 1
    a = Book.objects.all().order_by('-date')[(page_num - 1) * 10:page_num * 10]
    return render(request,'book/index.html',{'information':a,'total_page':total_page,'now_page':page_num})

@csrf_exempt
def postbox(request):
    if request.method == "POST":
        onedrive_data = json.loads(request.body)
        if onedrive_data['name'][-5] == '.':
            file_name,file_format = onedrive_data['name'][:-5],onedrive_data['name'][-4:]
        elif onedrive_data['name'][-4] == '.':
            file_name,file_format = onedrive_data['name'][:-4],onedrive_data['name'][-3:]
        else:
            h = HttpResponse('后缀名不合法')
            h.status = 404
            return h
        if (file_format != 'epub') and (file_format != 'mobi') and (file_format != 'azw3') and (file_format != 'pdf') and (file_format != 'kfx'):
            h = HttpResponse('后缀名不合法')
            h.status = 404
            return h
        if Book.objects.filter(file_name=file_name):    #如果存在这本书
            b = Book.objects.get(file_name=file_name)
            b.save_url(onedrive_data['url'],file_format,onedrive_data['size'])
            b.save()
        else:                                           #如果不存在这本书
            douban_data = get_book_data(file_name)
            pprint(douban_data)
            b = Book()
            b.date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if douban_data:
                b.file_name = file_name
                b.title = douban_data['title']
                if douban_data['subtitle']:
                    b.subtitle = douban_data['subtitle']
                if douban_data['alt_title']:
                    b.english_title = douban_data['alt_title']
                b.save()        #为添加作者准备
                author = douban_data.get('author')
                if author:       #如果作者不为空
                    if len(author) == 1:
                        a_inf = douban_data['author_intro']
                    else:
                        a_inf = douban_data['author_intro'].split('\n')[1::2]
                    al = []
                    if len(a_inf) == len(douban_data['author']):
                        a_inf = a_inf
                    else:
                        a_inf = ['不详' for i in range(len(douban_data['author']))]
                    for i in range(len(douban_data['author'])):
                        d = {}
                        d['name'] = douban_data['author'][i]
                        d['information'] = a_inf[i]
                        al.append(d)
                    for l in al:
                        a = None
                        if not Author.objects.filter(name = l['name']):     #添加作者
                            a = Author()
                            a.name = l['name']
                            a.information = l['information']
                            a.save()
                            a.book.add(b)
                        else:
                            a = Author.objects.get(name = l['name'])
                            a.book.add(b)
                        b.author.add(a)
                if douban_data.get('price'):
                    b.price = douban_data['price']
                b.cover = 'https://images.weserv.nl/?url=' + douban_data['images']['small'][8:]
                b.large_cover = 'https://images.weserv.nl/?url=' + douban_data['images']['large'][8:]
                b.summary = douban_data['summary']
                b.catalog = douban_data['catalog']
                if not Publisher.objects.filter(name = douban_data['publisher']):   #添加出版社
                    p = Publisher(name=douban_data['publisher'])
                    p.save()
                else:
                    p=Publisher.objects.get(name=douban_data['publisher'])
                b.publisher.add(p)
                p.book.add(b)
                b.save()
                b.douban_id = douban_data['id']
                if douban_data['isbn10']:
                    b.isbn10 = douban_data['isbn10']
                if douban_data['isbn13']:
                    b.isbn13 = douban_data['isbn13']
                if douban_data['pages']:
                    b.pages = douban_data['pages']
                if douban_data.get('tags'):
                    b.save()
                    for d_t in douban_data['tags']:
                        t = Tag()
                        t.name = d_t['name']
                        t.title = d_t['title']
                        t.save()
                        t.book.add(b)
                        b.tags.add(t)
                s = douban_data.get('series')
                if s and type(s) == type({}):
                    b.save()
                    s = Series()
                    s.name = douban_data.get('series')['title']
                    s.save()
                    s.book.add(b)
                    b.series.add(s)
                tr = douban_data.get('translator')
                pprint(tr)
                if tr and type(tr) == type([]):
                    b.save()
                    for tr in tr:
                        if not Translator.objects.filter(name=tr):
                            t = Translator()
                            t.name = tr
                            t.save()
                            t.book.add(b)
                            b.translator.add(t)
                        else:
                            b.translator.add(Translator.objects.get(name=tr))
                b.save_url(onedrive_data['url'],file_format,onedrive_data['size'])
            else:
                b.file_name = b.title = file_name
                b.save_url(onedrive_data['url'],file_format,onedrive_data['size'])
        b.save()
        return render(request,'book/404.html')
    else:
        return render(request,'book/404.html',status = 404)

def page_not_found(request, exception):
    return render(request,'book/404.html',status=404)
