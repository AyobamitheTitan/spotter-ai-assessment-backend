from rest_framework import serializers

class DirectionsSerializer(serializers.Serializer):
    coordinates = serializers.ListField()
    distance = serializers.FloatField()
    duration = serializers.FloatField()
    steps = serializers.ListField()