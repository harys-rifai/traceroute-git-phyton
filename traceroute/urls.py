from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'traceroutes', views.TracerouteViewSet)

urlpatterns = [
    path('wan/', views.wan_status, name='wan-status'),
    path('api/wan/', views.wan_status_api, name='wan-status-api'),
    *router.urls,
    path('<str:target>/', views.traceroute_result, name='traceroute-result'),
]