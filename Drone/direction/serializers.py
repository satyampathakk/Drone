from rest_framework import serializers
from .models import UserDestination,LocationUpdate

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model =LocationUpdate
        fields = ['latitude','longitude','user']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserDestination
        fields =['name', 'desired_lat','desired_long','timeStamp','user']