from rest_framework import serializers

class EnergyUsageSerializer(serializers.Serializer):
    location_id = serializers.IntegerField()
    date = serializers.DateField()

class LocationDateSerializer(serializers.Serializer):
    location_id = serializers.IntegerField()
    date = serializers.DateField(format='%Y-%m') # type: ignore