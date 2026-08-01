from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from datacenter.models import Datacenter
from datacenter.serializers import DatacenterSerializer


class DatacenterViewSet(ModelViewSet):
    queryset = Datacenter.objects.all()
    serializer_class = DatacenterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'provider', 'tier']