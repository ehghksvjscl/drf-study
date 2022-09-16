from django.contrib.auth.models import User
from django.db import models

TEAM_LIST = (
    ("FINANCE_TEAM", "FINANCE_TEAM"),
    ("SECURITY_TECH_TEAM", "SECURITY_TECH_TEAM"),
    ("SECURITY_TEAM", "SECURITY_TEAM"),
    ("LEGAL_TEAM", "LEGAL_TEAM"),
)


class Contract(models.Model):
    title = models.CharField(max_length=256, verbose_name="제목")
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="계약 담당자")
    is_private = models.BooleanField(default=True, verbose_name="비공개 여부")

    class Meta:
        db_table = "contract"
        verbose_name = "계약"
        verbose_name_plural = "계약 목록"


class Review(models.Model):
    team = models.CharField(max_length=255, choices=TEAM_LIST, verbose_name="팀 소속")
    manager = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, verbose_name="계약 담당자")
    contract = models.ForeignKey(Contract, null=True, verbose_name="승인 여부", on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False, verbose_name="승인 여부")
    
    class Meta:
        db_table = "review"
        verbose_name = "리뷰"
        verbose_name_plural = "리뷰 목록"