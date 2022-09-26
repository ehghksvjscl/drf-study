from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class TeamChoices(models.TextChoices):
        FINANCE_TEAM = ("FINANCE_TEAM", "재무팀")
        SECURITY_TECH_TEAM = ("SECURITY_TECH_TEAM", "보안기술팀")
        SECURITY_TEAM = ("SECURITY_TEAM", "보안팀")
        LEGAL_TEAM = ("LEGAL_TEAM", "법무팀")
        NO_TEAM = ("NO_TEAM", "팀없음")

    team = models.CharField(max_length=50, choices=TeamChoices.choices)
