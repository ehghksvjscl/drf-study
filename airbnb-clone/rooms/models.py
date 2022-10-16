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
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=150)
    is_pet_friendly = models.BooleanField(default=True)
    kind = models.CharField(max_length=50, choices=KindChoices.choices)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amenities = models.ManyToManyField("Amenity")
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def total_amenities(room):
        return room.amenities.count()

    def rating(room):
        review_count = room.reviews.count()
        if review_count == 0:
            return "No Review"
        else:
            total_rating = 0
            for review in room.reviews.all().values("rating"):
                total_rating = review.get("rating")

            return round(total_rating / review_count, 2)

    def __str__(self) -> str:
        return self.name


class Amenity(BaseTimeTamplate):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
