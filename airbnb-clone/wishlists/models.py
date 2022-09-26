from django.db import models
from common.models import BaseTimeTamplate
from django.contrib.auth import get_user_model


class Wishlist(BaseTimeTamplate):
    """wishlist 모델링"""

    name = models.CharField(max_length=150)
    rooms = models.ManyToManyField("rooms.Room")
    experiences = models.ManyToManyField("experiences.Experience")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
