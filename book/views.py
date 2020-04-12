from django.shortcuts import render
from django.http import HttpResponse
import json
import time
from django.views.decorators.csrf import csrf_exempt
from book.models import Book

# Create your views here.
def index(request):
    return render(request,'book/index.html')

@csrf_exempt
def postbox(request):
    if request.method == "POST":
        d = json.loads(request.body)
        d_l = d['name'].split('.')[0]
        name,format = d_l[0],d_l[1]
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if Book().objects.filter(name=name):
            b = Book().objects.get(name=name)
            if format == 'epub':
                b.epub_download_url = d['url']
            if format == 'azw3':
                b.azw3_download_url = d['url']
            if format == 'pdf':
                b.pdf_download_url = d['url']
            if format == 'mobi':
                b.mobi_download_url = d['url']
        else:
            b = Book(name = name,
                 file_idm=d['idm'],
                 date=date)
            if format == 'epub':
                b.epub_download_url = d['url']
            if format == 'azw3':
                b.azw3_download_url = d['url']
            if format == 'pdf':
                b.pdf_download_url = d['url']
            if format == 'mobi':
                b.mobi_download_url = d['url']
        b.save()