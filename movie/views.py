from django.shortcuts import render
from django.http import HttpResponse
import json
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def postbox(request):
    if(request.method == 'POST'):
        a = dict(request.POST)
    return HttpResponse(str(a))