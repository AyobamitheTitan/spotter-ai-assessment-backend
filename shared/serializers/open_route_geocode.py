from typing import Tuple
from rest_framework import serializers


class GeometrySerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    coordinates = serializers.ListField(child=serializers.FloatField())


class PropertiesSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    gid = serializers.CharField(required=False)
    layer = serializers.CharField(required=False)
    source = serializers.CharField(required=False)
    source_id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    confidence = serializers.FloatField(required=False)
    match_type = serializers.CharField(required=False)
    accuracy = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    country_gid = serializers.CharField(required=False)
    country_a = serializers.CharField(required=False)
    region = serializers.CharField(required=False)
    region_gid = serializers.CharField(required=False)
    region_a = serializers.CharField(required=False)
    county = serializers.CharField(required=False)
    county_gid = serializers.CharField(required=False)
    county_a = serializers.CharField(required=False)
    locality = serializers.CharField(required=False)
    locality_gid = serializers.CharField(required=False)
    neighbourhood = serializers.CharField(required=False)
    neighbourhood_gid = serializers.CharField(required=False)
    continent = serializers.CharField(required=False)
    continent_gid = serializers.CharField(required=False)
    label = serializers.CharField(required=False)
    bbox = serializers.ListField(child=serializers.FloatField(), required=False)


class FeatureSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    geometry = GeometrySerializer()
    properties = PropertiesSerializer()
    bbox = serializers.ListField(child=serializers.FloatField(), required=False)


class QueryLangSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    iso6391 = serializers.CharField(required=False)
    iso6393 = serializers.CharField(required=False)
    via = serializers.CharField(required=False)
    defaulted = serializers.BooleanField()


class ParsedTextSerializer(serializers.Serializer):
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    country = serializers.CharField(required=False)


class QuerySerializer(serializers.Serializer):
    text = serializers.CharField()
    size = serializers.IntegerField()
    layers = serializers.ListField(child=serializers.CharField(), required=False)
    private = serializers.BooleanField(required=False)
    lang = QueryLangSerializer()
    querySize = serializers.IntegerField(required=False)
    parser = serializers.CharField(required=False)
    parsed_text = ParsedTextSerializer()


class EngineSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    author = serializers.CharField(required=False)
    version = serializers.CharField(required=False)


class GeocodingSerializer(serializers.Serializer):
    version = serializers.CharField(required=False)
    attribution = serializers.CharField(required=False)
    query = QuerySerializer()
    warnings = serializers.ListField(child=serializers.CharField())
    engine = EngineSerializer()
    timestamp = serializers.FloatField(required=False)


class OpenRouteServiceGeocodeResponseSerializer(serializers.Serializer):
    geocoding = GeocodingSerializer()
    type = serializers.CharField(required=False)
    features = FeatureSerializer(many=True)
    bbox = serializers.ListField(child=serializers.FloatField())

    def get_coordinates(self):
        """Return a list of coordinates from all features."""
        features = self.validated_data.get("features", [])
        return [feature["geometry"]["coordinates"] for feature in features]

    def get_main_coordinates(self) -> None | Tuple[int, int]:
        """Return the coordinates of the most confident feature."""
        features = self.validated_data.get("features", [])
        main_feature = next((f for f in features), None)
        return main_feature["geometry"]["coordinates"] if main_feature else None
