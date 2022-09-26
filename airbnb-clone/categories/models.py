from django.db import models
from common.models import BaseTimeTamplate


class Category(BaseTimeTamplate):
    class CategoryKindChoices(models.TextChoices):
        ROOMSM = ("rooms", "Rooms")
        EXPERIENCES = ("experiences", "Experiences")

    name = models.CharField(max_length=150, default="")
    kind = models.CharField(max_length=50, choices=CategoryKindChoices.choices)

    def __str__(self) -> str:
        return f"{self.kind.title()} - {self.name}"

    class Meta:
        verbose_name_plural = "Categories"
