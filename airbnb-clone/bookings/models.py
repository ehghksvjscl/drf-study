from django.db import models
from common.models import BaseTimeTamplate
from django.contrib.auth import get_user_model


class Booking(BaseTimeTamplate):
    """Booking 모델링"""

    class BookingKindChoices(models.TextChoices):
        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(max_length=15, choices=BookingKindChoices.choices)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.SET_NULL, null=True, blank=True
    )
    experience = models.ForeignKey(
        "experiences.Experience", on_delete=models.SET_NULL, null=True, blank=True
    )
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    experience_time = models.DateTimeField(null=True, blank=True)
    guests = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.kind} / {self.user}"
