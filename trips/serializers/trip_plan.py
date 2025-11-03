from rest_framework import serializers


class TripRouteSummanySerializer(serializers.Serializer):
    distance = serializers.FloatField()
    duration = serializers.FloatField()


class RouteStepSerializer(TripRouteSummanySerializer):
    instruction = serializers.CharField()
    type = serializers.IntegerField()
    name = serializers.CharField()
    way_points = serializers.ListField(child=serializers.IntegerField())


class RouteSegmentsSerializer(TripRouteSummanySerializer):
    steps = serializers.ListField(child=RouteStepSerializer())


class TripRouteSerializer(serializers.Serializer):
    summary = TripRouteSummanySerializer()
    segments = RouteSegmentsSerializer()
    bbox = serializers.ListField(
        child=serializers.FloatField(),
        min_length=4,
        max_length=4,
        help_text="Bounding box [min_lon, min_lat, max_lon, max_lat].",
    )
    geometry = serializers.CharField()
    waypoints = serializers.ListField(child=serializers.IntegerField())


class TripPlanSerializer(serializers.Serializer):
    bbox = serializers.ListField(
        child=serializers.FloatField(),
        min_length=4,
        max_length=4,
        help_text="Bounding box [min_lon, min_lat, max_lon, max_lat].",
    )
    routes = serializers.ListField(child=TripRouteSerializer())
    # metadata too, but that's not too important
