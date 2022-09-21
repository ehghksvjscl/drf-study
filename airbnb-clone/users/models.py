from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korea")
        EN = ("en", "Engish")

    class CurrenyChoices(models.TextChoices):
        KRW = ("krw", "KRW")
        USD = ("usd", "USD")

    first_name = models.CharField(max_length=150, blank=True, editable=False)
    last_name = models.CharField(max_length=150, blank=True, editable=False)
    name = models.CharField(default="", max_length=150, verbose_name="이름")
    is_host = models.BooleanField(default=False, verbose_name="호스트 여부")
    avatar = models.ImageField(blank=True)
    gender = models.CharField(max_length=6, choices=GenderChoices.choices)
    language = models.CharField(
        max_length=2, choices=LanguageChoices.choices, default=LanguageChoices.KR
    )
    curreny = models.CharField(
        max_length=3, choices=CurrenyChoices.choices, default=CurrenyChoices.KRW
    )
