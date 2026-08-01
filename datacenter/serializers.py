from rest_framework import serializers

from datacenter.models import Datacenter


class DatacenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datacenter
        fields = '__all__'