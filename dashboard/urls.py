from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('api/stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('unified/', views.UnifiedDashboardView.as_view(), name='unified-dashboard'),
    path('unified/api/stats/', views.UnifiedDashboardStatsView.as_view(), name='unified-dashboard-stats'),
    path('animations/', views.AnimationsView.as_view(), name='animations'),
]
