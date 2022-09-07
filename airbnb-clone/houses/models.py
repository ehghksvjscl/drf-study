from django.db import models

class House(models.Model):
    """House Model Difinition"""

    name = models.CharField(max_length=140)
    price = models.PositiveBigIntegerField(default=0)
    description = models.TextField()
    address = models.CharField(max_length=140)
    pet_allowed = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name