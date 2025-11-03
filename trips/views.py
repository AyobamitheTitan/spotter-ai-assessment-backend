from shared.views.base import BaseAPIView
from trips.models import TripModel, TripDetailsModel
from trips.serializers.trips import CreateTripSerializer, TripDetailsSerializer
from trips.services.trips import TripService
from trips.services.trip_details import TripDetailsService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException


# Create your views here.
class TripApiView(BaseAPIView):
    model_class = TripModel
    serializer_class = CreateTripSerializer
    service_class = TripService

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data = self.service_class.create(serializer.validated_data)
        return Response(data, status=status.HTTP_201_CREATED)


class TripDetailsApiView(BaseAPIView):
    model_class = TripDetailsModel
    serializer_class = TripDetailsSerializer
    service_class = TripDetailsService

    http_method_names = ["get", "head", "options"]


class TripDetailsByTripIdApiView(BaseAPIView):
    model_class = TripDetailsModel
    serializer_class = TripDetailsSerializer
    service_class = TripDetailsService

    http_method_names = ["get", "head", "options"]

    def get(self, request, *args, **kwargs):
        trip_id = kwargs.get("trip_id")
        if not trip_id:
            raise APIException([], 400)
        queryset = self.service_class.get_by_trip_id(trip_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response({"data": serializer.data, "message": "Retrieved"})
