from rest_framework import serializers
from .models import DnsQuery


class DnsQuerySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DnsQuery
        fields = '__all__'
