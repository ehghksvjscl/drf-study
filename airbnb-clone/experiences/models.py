from django.db import models
from django.contrib.auth import get_user_model

from common.models import BaseTimeTamplate


class Experience(BaseTimeTamplate):
    """경험 모델 정의"""

    class KindChoices(models.TextChoices):
        ENTRIE_PLACE = ("entire_place", "Entire_place")
        PRIVATE_ROOM = ("private_room", "Private_room")
        SHARED_ROOM = ("shared_room", "Shared_room")

    name = models.CharField(max_length=150, default="")
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=50, default="서울")
    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)
    address = models.CharField(max_length=150)
    start = models.TimeField()
    end = models.TimeField()
    perks = models.ManyToManyField("Perk")

    def __str__(self) -> str:
        return self.name


class Perk(BaseTimeTamplate):
    name = models.CharField(max_length=150, default="")
    detail = models.CharField(max_length=250, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
