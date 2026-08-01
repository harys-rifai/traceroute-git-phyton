from rest_framework.routers import DefaultRouter

from datacenter import views

router = DefaultRouter()
router.register(r'datacenters', views.DatacenterViewSet)

urlpatterns = router.urls