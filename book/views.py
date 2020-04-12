from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request,'book/index.html')

@csrf_exempt
def postbox(request):
    if request.method == "POST":
        d = json.load(request.body)