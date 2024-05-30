from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Attack
from .serializers import ProjectSerializer

def xss_attack(request):
    #xss.delay()
    return

def sqli_attack(request):
    #sqli.delay()
    return 
