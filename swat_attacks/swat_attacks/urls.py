from django.contrib import admin
from django.urls import path, include
from tasks.views import xss_attack,sqli_attack

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls'))
]
