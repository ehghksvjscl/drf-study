from django.db import models
from common.models import BaseTimeTamplate
from django.contrib.auth import get_user_model


class Photo(BaseTimeTamplate):
    """Booking 모델링"""

    file = models.ImageField()
    description = models.CharField(max_length=140)
    room = models.ForeignKey(
        "rooms.Room", null=True, blank=True, on_delete=models.CASCADE
    )
    experience = models.ForeignKey(
        "experiences.Experience", null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return "photo file"


class Video(BaseTimeTamplate):
    file = models.FileField()
    experience = models.OneToOneField(
        "experiences.Experience", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return "video file"
