from django.urls import path
from dashboard import consumers

websocket_urlpatterns = [
    path('ws/dashboard/', consumers.DashboardConsumer.as_asgi()),
    path('ws/traceroute/', consumers.TracerouteConsumer.as_asgi()),
]
