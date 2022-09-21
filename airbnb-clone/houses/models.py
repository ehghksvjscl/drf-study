from django.db import models
from django.contrib.auth import get_user_model


class House(models.Model):
    """House Model Difinition"""

    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name="집주인"
    )
    name = models.CharField(max_length=140)
    price = models.PositiveBigIntegerField(default=0)
    description = models.TextField()
    address = models.CharField(max_length=140)
    pet_allowed = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
