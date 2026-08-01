from rest_framework import serializers

from servers.models import Server


class ServerSerializer(serializers.ModelSerializer):
    datacenter = serializers.StringRelatedField()

    class Meta:
        model = Server
        fields = '__all__'
