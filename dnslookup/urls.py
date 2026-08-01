from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'dns', views.DnsQueryViewSet)

urlpatterns = router.urls
