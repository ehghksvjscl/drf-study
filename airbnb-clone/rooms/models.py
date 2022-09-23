from django.db import models
from django.contrib.auth import get_user_model

from common.models import BaseTimeTamplate


class Room(BaseTimeTamplate):
    class KindChoices(models.TextChoices):
        ENTRIE_PLACE = ("entire_place", "Entire_place")
        PRIVATE_ROOM = ("private_room", "Private_room")
        SHARED_ROOM = ("shared_room", "Shared_room")
        
    name = models.CharField(max_length=150, default="")
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=50, default="서울")
    price = models.PositiveBigIntegerField(default=0)
    rooms = models.PositiveSmallIntegerField(default=0)
    toilets = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    address = models.CharField(max_length=150)
    is_pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=50, choices=KindChoices.choices)
    onwer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amenitys = models.ManyToManyField("Amenity")


class Amenity(BaseTimeTamplate):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name