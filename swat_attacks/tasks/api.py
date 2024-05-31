from .models import Attack
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import ProjectSerializer
from .tasks import xss, sqli

class ProjectViewSet(viewsets.ModelViewSet):
   queryset = Attack.objects.all()
   permission_classes = [permissions.AllowAny]
   serializer_class = ProjectSerializer
   
   def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Llama al método personalizado para la segunda ruta
        xss.delay(request.data)

        return Response(status=status.HTTP_201_CREATED)
   
  
class ProjectViewSet1(viewsets.ModelViewSet):
   queryset = Attack.objects.all()
   permission_classes = [permissions.AllowAny]
   serializer_class = ProjectSerializer
   
   #sqli.delay()