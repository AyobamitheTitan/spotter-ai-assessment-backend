from django.urls import path

from trips.views import TripApiView, TripDetailsApiView, TripDetailsByTripIdApiView

trips_view = TripApiView.as_view()
trip_details_view = TripDetailsApiView.as_view()
trip_details_trip_id_view = TripDetailsByTripIdApiView.as_view()

urlpatterns = [
    path("trips", trips_view, name="Trips"),
    path("trip-details", trip_details_view, name="Trip details"),
    path("trip-details/<uuid:pk>", trip_details_view, name="Trip details"),
    path(
        "trip-details/trip/<uuid:trip_id>",
        trip_details_trip_id_view,
        name="Trip details by trip id",
    ),
    path("trips/<uuid:pk>", trips_view, name="Trip"),
]
