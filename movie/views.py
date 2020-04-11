from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from movie.models import Movie

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def postbox(request):
    if request.method == 'POST':
        d = json.loads(request.body)
        d = d['date']
        m = Movie(name=d['name'],file_idm=d['idm'],download_url=d['url'])
        m.save()