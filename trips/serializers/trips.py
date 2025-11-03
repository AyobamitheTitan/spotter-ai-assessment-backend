from rest_framework.serializers import ModelSerializer, SerializerMethodField

from trips.models import TripModel, TripDetailsModel


class CreateTripSerializer(ModelSerializer):
    class Meta:
        model = TripModel
        fields = [
            "id",
            "current_location",
            "pickup_location",
            "dropoff_location",
            "current_cycle_used_hrs",
        ]
        read_only_fields = ["read_only_fields"]


class TripDetailsSerializer(ModelSerializer):
    total_steps = SerializerMethodField()
    main_summary = SerializerMethodField()

    class Meta:
        model = TripDetailsModel
        fields = [
            "id",
            "origin",
            "pickup",
            "dropoff",
            "trip",
            "distance",
            "duration",
            "bbox",
            "geometry",
            "steps",
            "created_at",
            "total_steps",
            "main_summary",
        ]
        read_only_fields = ["id", "created_at", "total_steps", "main_summary"]

    def get_total_steps(self, obj):
        return obj.total_steps()

    def get_main_summary(self, obj):
        return obj.main_summary()
