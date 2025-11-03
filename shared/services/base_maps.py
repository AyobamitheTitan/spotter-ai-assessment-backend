from typing import Tuple

from shared.serializers.directions import DirectionsSerializer


class MapsApiService:

    @classmethod
    def geocode(cls, location: str) -> Tuple[int, int]:
        """
        Returns geocode representation of a given location
        (longitude and latitude)
        """
        return (4.1331082, 5.331790)

    @classmethod
    def directions(
        cls,
        origin: Tuple[int, int],
        passthrough: Tuple[int, int],
        destination: Tuple[int, int],
    ) -> DirectionsSerializer:
        """
        Returns directions to a destination from a given origin
        """
        return DirectionsSerializer()
