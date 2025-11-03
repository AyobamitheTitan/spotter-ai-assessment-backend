from typing import Tuple
from rest_framework import serializers


class GeometrySerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField(child=serializers.FloatField())


class PropertiesSerializer(serializers.Serializer):
    id = serializers.CharField()
    gid = serializers.CharField()
    layer = serializers.CharField()
    source = serializers.CharField()
    source_id = serializers.CharField()
    name = serializers.CharField()
    confidence = serializers.FloatField(required=False)
    match_type = serializers.CharField(required=False)
    accuracy = serializers.CharField(required=False)
    country = serializers.CharField()
    country_gid = serializers.CharField()
    country_a = serializers.CharField()
    region = serializers.CharField()
    region_gid = serializers.CharField()
    region_a = serializers.CharField(required=False)
    county = serializers.CharField(required=False)
    county_gid = serializers.CharField(required=False)
    county_a = serializers.CharField(required=False)
    locality = serializers.CharField(required=False)
    locality_gid = serializers.CharField(required=False)
    neighbourhood = serializers.CharField(required=False)
    neighbourhood_gid = serializers.CharField(required=False)
    continent = serializers.CharField()
    continent_gid = serializers.CharField()
    label = serializers.CharField()
    bbox = serializers.ListField(child=serializers.FloatField(), required=False)


class FeatureSerializer(serializers.Serializer):
    type = serializers.CharField()
    geometry = GeometrySerializer()
    properties = PropertiesSerializer()
    bbox = serializers.ListField(child=serializers.FloatField(), required=False)


class QueryLangSerializer(serializers.Serializer):
    name = serializers.CharField()
    iso6391 = serializers.CharField()
    iso6393 = serializers.CharField()
    via = serializers.CharField()
    defaulted = serializers.BooleanField()


class ParsedTextSerializer(serializers.Serializer):
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    country = serializers.CharField(required=False)


class QuerySerializer(serializers.Serializer):
    text = serializers.CharField()
    size = serializers.IntegerField()
    layers = serializers.ListField(child=serializers.CharField())
    private = serializers.BooleanField()
    lang = QueryLangSerializer()
    querySize = serializers.IntegerField()
    parser = serializers.CharField()
    parsed_text = ParsedTextSerializer()


class EngineSerializer(serializers.Serializer):
    name = serializers.CharField()
    author = serializers.CharField()
    version = serializers.CharField()


class GeocodingSerializer(serializers.Serializer):
    version = serializers.CharField()
    attribution = serializers.CharField()
    query = QuerySerializer()
    warnings = serializers.ListField(child=serializers.CharField())
    engine = EngineSerializer()
    timestamp = serializers.FloatField()


class OpenRouteServiceGeocodeResponseSerializer(serializers.Serializer):
    geocoding = GeocodingSerializer()
    type = serializers.CharField()
    features = FeatureSerializer(many=True)
    bbox = serializers.ListField(child=serializers.FloatField())

    def get_coordinates(self):
        """Return a list of coordinates from all features."""
        features = self.validated_data.get("features", [])
        return [feature["geometry"]["coordinates"] for feature in features]

    def get_main_coordinates(self) -> None | Tuple[int, int]:
        """Return the coordinates of the most confident feature."""
        features = self.validated_data.get("features", [])
        main_feature = next(
            (f for f in features), None
        )
        return main_feature["geometry"]["coordinates"] if main_feature else None
