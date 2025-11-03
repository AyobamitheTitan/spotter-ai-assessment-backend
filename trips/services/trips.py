import threading
from shared.serializers.open_route_directions import (
    OpenRouteDirectionResponseSerializer,
)
from shared.services.base import BaseApiService
from shared.services.open_route_maps import OpenRouteMapsApiService
from trips.repositories.trips import TripRepository, TripDetailsRepository


class TripService(BaseApiService):
    repository_class = TripRepository
    maps_service = OpenRouteMapsApiService

    @classmethod
    def create(cls, validated_data):
        current_location_geocoded = cls.maps_service.geocode(
            validated_data["current_location"]
        )
        pickup_location_geocoded = cls.maps_service.geocode(
            validated_data["pickup_location"]
        )
        dropoff_location_geocoded = cls.maps_service.geocode(
            validated_data["dropoff_location"]
        )

        directions = cls.maps_service.directions(
            current_location_geocoded,
            pickup_location_geocoded,
            dropoff_location_geocoded,
        )
        trip = super().create(validated_data)
        route = directions.validated_data["routes"][0]
        segment = route["segments"][0]
        decoded_geometry = OpenRouteDirectionResponseSerializer.decode_polyline(
            route["geometry"]
        )

        trip_details = {
            "origin": current_location_geocoded,
            "pickup": pickup_location_geocoded,
            "dropoff": dropoff_location_geocoded,
            "trip_id": trip.id,
            "geometry": decoded_geometry,
            "distance": route["summary"]["distance"],
            "duration": route["summary"]["duration"],
            "bbox": route["bbox"],
            "steps": [
                {
                    "instruction": step["instruction"],
                    "distance": step["distance"],
                    "duration": step["duration"],
                }
                for step in segment["steps"]
            ],
        }

        threading.Thread(
            target=TripDetailsRepository.create, kwargs=trip_details
        ).start()

        return trip_details
