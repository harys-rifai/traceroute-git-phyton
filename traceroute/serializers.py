from rest_framework import serializers
from .models import Traceroute, TracerouteHop


class TracerouteHopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TracerouteHop
        fields = '__all__'


class TracerouteSerializer(serializers.ModelSerializer):
    hops = TracerouteHopSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Traceroute
        fields = '__all__'