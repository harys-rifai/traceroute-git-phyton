from rest_framework.routers import DefaultRouter

from servers import views

router = DefaultRouter()
router.register(r'servers', views.ServerViewSet)

urlpatterns = router.urls
