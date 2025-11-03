from shared.repositories.base import BaseRepository
from trips.models import TripModel, TripDetailsModel


class TripRepository(BaseRepository):
    model = TripModel


class TripDetailsRepository(BaseRepository):
    model = TripDetailsModel
