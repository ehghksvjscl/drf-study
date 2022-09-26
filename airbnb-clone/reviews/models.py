from django.db import models
from common.models import BaseTimeTamplate
from django.contrib.auth import get_user_model


class Review(BaseTimeTamplate):
    """리뷰 모델링"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(
        "rooms.Room", null=True, blank=True, on_delete=models.CASCADE
    )
    experience = models.ForeignKey(
        "experiences.Experience", null=True, blank=True, on_delete=models.CASCADE
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐"
