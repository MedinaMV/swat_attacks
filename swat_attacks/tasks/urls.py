from rest_framework import routers
from .api import ProjectViewSet

router = routers.DefaultRouter()

router.register('api/attack', ProjectViewSet, 'attack')

urlpatterns = router.urls