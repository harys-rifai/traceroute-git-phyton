from django.urls import path, include, re_path
from django.contrib import admin
from django.shortcuts import redirect
from core.admin import dashboard_view
from dashboard.views import AnimationsView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from traceroute.views import traceroute_result

schema_view = get_schema_view(
   openapi.Info(
      title="Network Globe Scanner API",
      default_version='v1',
      description="API for Network Globe Scanner - Traceroute, DNS, Datacenter Management",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', lambda request: redirect('unified-dashboard')),
    path('admin/dashboard/', dashboard_view, name='admin-dashboard'),
    re_path(r'^admin/$', lambda request: redirect('admin-dashboard')),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/traceroute/', include('traceroute.urls')),
    path('traceroute/<str:target>/', traceroute_result, name='traceroute-result'),
    path('api/dns/', include('dnslookup.urls')),
    path('api/datacenters/', include('datacenter.urls')),
    path('api/servers/', include('servers.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('animations/', AnimationsView.as_view(), name='animations'),
    path('api/', include('api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
