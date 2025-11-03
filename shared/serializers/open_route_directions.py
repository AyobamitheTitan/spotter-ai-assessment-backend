from rest_framework import serializers


class StepSerializer(serializers.Serializer):
    distance = serializers.FloatField()
    duration = serializers.FloatField()
    type = serializers.IntegerField()
    instruction = serializers.CharField()
    name = serializers.CharField()
    way_points = serializers.ListField(child=serializers.IntegerField())
    exit_number = serializers.IntegerField(required=False)


class SegmentSerializer(serializers.Serializer):
    distance = serializers.FloatField()
    duration = serializers.FloatField()
    steps = StepSerializer(many=True)


class SummarySerializer(serializers.Serializer):
    distance = serializers.FloatField()
    duration = serializers.FloatField()


class RouteSerializer(serializers.Serializer):
    summary = SummarySerializer()
    segments = SegmentSerializer(many=True)
    bbox = serializers.ListField(child=serializers.FloatField())
    geometry = serializers.CharField()


class OpenRouteDirectionResponseSerializer(serializers.Serializer):
    bbox = serializers.ListField(child=serializers.FloatField())
    routes = RouteSerializer(many=True)

    @staticmethod
    def decode_polyline(geometry):
        """
        Decodes an encoded polyline string into a list of [lon, lat] coordinate pairs.
        Based on Google's Encoded Polyline Algorithm.
        """
        coords = []
        index = 0
        lat = 0
        lon = 0
        length = len(geometry)

        while index < length:
            for coord_index in range(2):  # decode latitude and longitude alternately
                result = 0
                shift = 0
                while True:
                    b = ord(geometry[index]) - 63
                    index += 1
                    result |= (b & 0x1F) << shift
                    shift += 5
                    if b < 0x20:
                        break
                delta = ~(result >> 1) if result & 1 else (result >> 1)
                if coord_index == 0:
                    lat += delta
                else:
                    lon += delta
            coords.append([lon / 1e5, lat / 1e5])

        return coords
