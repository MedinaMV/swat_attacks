from django.shortcuts import render
from django.http import HttpResponse
from .tasks import xss,sqli

# Create your views here.
def xss_attack(request):
    xss.delay()
    return HttpResponse('<h1>Starting XSS Attack</h1>')

def sqli_attack(request):
    sqli.delay()
    return HttpResponse('<h1>Starting SQLi Attack</h1>')
