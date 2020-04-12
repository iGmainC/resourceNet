from django.http import HttpResponse
import json
from django.shortcuts import render
import time
from django.views.decorators.csrf import csrf_exempt
from book.models import Book
from django.http import Http404

# Create your views here.
def index(request):
    a = Book.objects.all().order_by('id')
    print(a)
    return render(request,'book/index.html',{'information':a})

@csrf_exempt
def postbox(request):
    if request.method == "POST":
        d = json.loads(request.body)
        d_l = d['name'].split('.')
        name,format = d_l[0],d_l[1]
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if Book.objects.filter(name=name):
            b = Book.objects.get(name=name)
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
    return HttpResponse('<h1>404</h1>')




def page_not_found(request, exception):
    return HttpResponse('404')