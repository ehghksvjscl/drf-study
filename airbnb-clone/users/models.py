from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, editable=False)
    last_name = models.CharField(max_length=150, blank=True, editable=False)
    name = models.CharField(default="", max_length=150, verbose_name="이름")
    is_host = models.BooleanField(default=False, verbose_name="호스트 여부")
