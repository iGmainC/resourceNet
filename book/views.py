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

#从豆瓣获取图书信息
def get_book_data(book_name):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.45'}
    #url = 'https://douban.uieee.com/v2/book/search'
    url = 'https://api.douban.com/v2/book/search'
    data_pack = {'q':book_name,'count': 1,'start':0,'apikey':'0b2bdeda43b5688921839c8ecb20399b'}
    data = requests.get(url,headers=headers,params=data_pack)
    if data.status_code != 200:
        return None
    else:
        data = json.loads(data.text)['books'][0]
        return data


# Create your views here.
def index(request):
    a = Book.objects.all().order_by('-date')
    print(a)
    return render(request,'book/index.html',{'information':a})

def detail(request,id):
    b = Book.objects.get(douban_id=id)
    print(b)
    return render(request,'book/detail.html',{'information':b})

@csrf_exempt
def postbox(request):
    if request.method == "POST":
        d = json.loads(request.body)
        pprint(d)
        d_l = d['name'].split('.')
        name,format = d_l[0],d_l[1]     #将书名和文件格式分离
        print(name)
        douban_data = get_book_data(name)
        pprint(douban_data)
        if douban_data == None:
            return HttpResponse('豆瓣数据获取失败')
        if Book.objects.filter(douban_id=douban_data['id']):    #用豆瓣id查询数据库
            b = Book.objects.get(douban_id=douban_data['id'])
            if format == 'epub' and b.epub_flag == False:
                b.epub_download_url = d['url']
            if format == 'azw3' and b.azw3_flag == False:
                b.azw3_download_url = d['url']
            if format == 'pdf' and b.pdf_flag:
                b.pdf_download_url = d['url']
            if format == 'mobi' and b.mobi_flag == False:
                b.mobi_download_url = d['url']
        else:
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            b = Book(book_name = douban_data['title'],
                     author = douban_data['author'][0],
                 file_idm=d['idm'],
                 douban_id=douban_data['id'],
                 cover_img_url='https://images.weserv.nl/?url=' + douban_data['image'][8:],
                 date=date)
            if format == 'epub':
                b.epub_download_url = d['url']
                b.epub_flag = True
            if format == 'azw3':
                b.azw3_download_url = d['url']
                b.azw3_flag = True
            if format == 'pdf':
                b.pdf_download_url = d['url']
                b.pdf_flag = True
            if format == 'mobi':
                b.mobi_download_url = d['url']
                b.mobi_flag = True
        b.save()
    return HttpResponse('<h1>404</h1>')

'''
data = {'alt': 'https://book.douban.com/subject/1012611/',
 'alt_title': 'The Crowd: A Study of the Popular Mind',
 'author': ['（法）勒庞'],
 'author_intro': '古斯塔夫・勒庞 Gustave Le Bon(1841-1931) '
                 '法国著名社会心理学家。他自1894年始，写下一系列社会心理学著作，以本书最为著名，被 '
                 '翻译成近二十种语言，至今仍在国际学术界有广泛影响。\n'
                 '\n',
 'binding': '平装',
 'catalog': '民主直通独裁的心理机制\n'
            '勒庞《乌合之众》的得与失\n'
            '作者前言\n'
            '导言：群体的时代\n'
            '第一卷 群体心理\n'
            '1．群体的一般特征\n'
            '2．群体的感情和道德观\n'
            '3．群体的观念、推理与想像力\n'
            '4．群体信仰所采取的宗教形式\n'
            '第二卷 群体的意见与信念\n'
            '1．群体的意见和信念中的间接因素\n'
            '2．群体意见的直接因素\n'
            '3．群体领袖及其说服的手法\n'
            '4．群体的信息和意见的变化范围\n'
            '第三卷 不同群体的分类及其特点\n'
            '1．群体的分类\n'
            '2．被称为犯罪群体的群体\n'
            '3．刑事案件的陪审团\n'
            '4．选民群体\n'
            '5．议会\n'
            '译名对照表',
 'id': '1012611',
 'image': 'https://img3.doubanio.com/view/subject/m/public/s1988393.jpg',
 'images': {'large': 'https://img3.doubanio.com/view/subject/l/public/s1988393.jpg',
            'medium': 'https://img3.doubanio.com/view/subject/m/public/s1988393.jpg',
            'small': 'https://img3.doubanio.com/view/subject/s/public/s1988393.jpg'},
 'isbn10': '7801093666',
 'isbn13': '9787801093660',
 'origin_title': 'The Crowd: A Study of the Popular Mind',
 'pages': '183',
 'price': '16.00元',
 'pubdate': '2011-5-1',
 'publisher': '中央编译出版社',
 'rating': {'average': '8.2', 'max': 10, 'min': 0, 'numRaters': 93933},
 'subtitle': '大众心理研究',
 'summary': '古斯塔夫・勒庞 Gustave Le Bon(1841-1931) '
            '法国著名社会心理学家。他自1894年始，写下一系列社会心理学著作，以本书最为著名；在社会心理学领域已有的著作中 ，最有影响的，也是这本并不很厚的《乌合之众》。古斯塔夫・勒庞在他在书中极为精致地描述了集体心态，对人们理解集体行为的作用以及对社会心理学的思考发挥了巨大影响。《乌合之众--大众心理研究》在西方已印至第29版，其观点新颖，语言生动，是群体行为的研究者不可不读的佳作。',
 'tags': [{'count': 22613, 'name': '心理学', 'title': '心理学'},
          {'count': 21199, 'name': '社会心理学', 'title': '社会心理学'},
          {'count': 17178, 'name': '群体心理学', 'title': '群体心理学'},
          {'count': 13517, 'name': '乌合之众', 'title': '乌合之众'},
          {'count': 13093, 'name': '大众心理', 'title': '大众心理'},
          {'count': 10360, 'name': '社会学', 'title': '社会学'},
          {'count': 7178, 'name': '心理', 'title': '心理'},
          {'count': 5938, 'name': '社会', 'title': '社会'}],
 'title': '乌合之众',
 'translator': ['冯克利'],
 'url': 'https://api.douban.com/v2/book/1012611'}
'''


def page_not_found(request, exception):
    return HttpResponse('404')