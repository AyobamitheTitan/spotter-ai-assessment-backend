from shared.services.base import BaseApiService
from trips.repositories.trips import TripDetailsRepository


class TripDetailsService(BaseApiService):
    repository_class = TripDetailsRepository

    @classmethod
    def get_by_trip_id(cls, trip_id):
        return cls.repository_class.get_by_filters({"trip_id": trip_id})
