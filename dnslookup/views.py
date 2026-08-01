from rest_framework import viewsets, permissions
from .models import DnsQuery
from .serializers import DnsQuerySerializer


class DnsQueryViewSet(viewsets.ModelViewSet):
    queryset = DnsQuery.objects.all()
    serializer_class = DnsQuerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
