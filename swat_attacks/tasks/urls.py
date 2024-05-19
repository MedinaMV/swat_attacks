from django.urls import path
from . import views

urlpatterns = [
    path('xss/', views.xss_attack),
    path('sqli/', views.sqli_attack)
]