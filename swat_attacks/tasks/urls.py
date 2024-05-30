from . import views
from rest_framework import routers
from .api import ProjectViewSet, ProjectViewSet1

router = routers.DefaultRouter()

router.register('api/xss', ProjectViewSet, 'xss')
router.register('api/sqli', ProjectViewSet1, 'sqli')

urlpatterns = router.urls