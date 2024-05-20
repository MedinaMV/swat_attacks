from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer

def xss_attack(request):
    if request.method == 'POST':
        data = request.POST
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            #xss.delay()
            print(serializer)
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def sqli_attack(request):
    #sqli.delay()
    return 
