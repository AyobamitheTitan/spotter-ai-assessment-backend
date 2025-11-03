from requests import get, post
from rest_framework import exceptions
from shared.serializers.open_route_directions import (
    OpenRouteDirectionResponseSerializer,
)
from shared.serializers.open_route_geocode import (
    OpenRouteServiceGeocodeResponseSerializer,
)
from shared.services.base_maps import MapsApiService
from django.conf import settings
import json


class OpenRouteMapsApiService(MapsApiService):
    @classmethod
    def geocode(cls, location):
        OPEN_ROUTE_API_KEY = getattr(settings, "OPEN_ROUTE_API_KEY", None)
        BASE_OPEN_ROUTE_URL = getattr(settings, "BASE_OPEN_ROUTE_URL", None)
        if (not OPEN_ROUTE_API_KEY) or (not BASE_OPEN_ROUTE_URL):
            raise exceptions.APIException(
                [
                    "Improper configuration: BASE_OPEN_ROUTE_URL or OPEN_ROUTE_API_KEY keys not set"
                ],
                500,
            )
        geocode_request = get(
            f"{BASE_OPEN_ROUTE_URL}/geocode/search",
            params={"api_key": OPEN_ROUTE_API_KEY, "text": location},
        )

        if not geocode_request.ok:
            raise exceptions.APIException(
                geocode_request.reason, geocode_request.status_code
            )
        response_to_json = json.loads(geocode_request.text)
        json_to_serializer = OpenRouteServiceGeocodeResponseSerializer(
            data=response_to_json
        )
        json_to_serializer.is_valid(raise_exception=True)

        return json_to_serializer.get_main_coordinates()

    @classmethod
    def directions(cls, origin, passthrough, destination):
        OPEN_ROUTE_API_KEY = getattr(settings, "OPEN_ROUTE_API_KEY", None)
        BASE_OPEN_ROUTE_URL = getattr(settings, "BASE_OPEN_ROUTE_URL", None)
        if (not OPEN_ROUTE_API_KEY) or (not BASE_OPEN_ROUTE_URL):
            raise exceptions.APIException(
                [
                    "Improper configuration: BASE_OPEN_ROUTE_URL or OPEN_ROUTE_API_KEY keys not set"
                ],
                500,
            )
        directions_request = post(
            f"{BASE_OPEN_ROUTE_URL}/v2/directions/driving-car",
            json={"coordinates": [origin, passthrough, destination]},
            headers={"Authorization": OPEN_ROUTE_API_KEY},
        )
        if not directions_request.ok:

            raise exceptions.APIException(
                directions_request.reason, directions_request.status_code
            )
        response_to_json = json.loads(directions_request.text)

        json_to_serializer = OpenRouteDirectionResponseSerializer(data=response_to_json)
        json_to_serializer.is_valid(raise_exception=True)

        return json_to_serializer
