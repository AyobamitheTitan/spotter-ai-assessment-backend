import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class TripModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    current_cycle_used_hrs = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip {self.id}: From {self.current_location} through {self.pickup_location} to {self.dropoff_location}"


class TripDetailsModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    trip = models.ForeignKey(TripModel, on_delete=models.CASCADE, related_name="steps")

    distance = models.FloatField(help_text="Total route distance in meters")
    duration = models.FloatField(help_text="Total route duration in seconds")

    bbox = ArrayField(
        models.FloatField(),
        size=4,
        null=True,
        blank=True,
        help_text="Bounding box: [min_lon, min_lat, max_lon, max_lat]",
    )

    origin = ArrayField(
        models.FloatField(),
        size=2,
        help_text="Geocode for origin location",
        default=[3, 2],
    )

    pickup = ArrayField(
        models.FloatField(),
        size=2,
        help_text="Geocode for pickup location",
        default=[3, 2],
    )

    dropoff = ArrayField(
        models.FloatField(),
        size=2,
        help_text="Geocode for dropoff location",
        default=[3, 2],
    )

    geometry = ArrayField(
        ArrayField(models.FloatField(), size=2),
        help_text="List of [lon, lat] coordinate pairs",
    )

    # Each step will be a JSON object like:
    # {"instruction": "Turn right", "distance": 120.5, "duration": 45.2}
    steps = models.JSONField(help_text="List of navigation steps")

    created_at = models.DateTimeField(auto_now_add=True)

    def total_steps(self):
        return len(self.steps) if self.steps else 0

    def main_summary(self):
        return {
            "distance_km": round(self.distance / 1000, 2),
            "duration_hr": round(self.duration / 3600, 2),
        }
