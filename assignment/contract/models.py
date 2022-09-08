from django.contrib.auth.models import User
from django.db import models


class Contract(models.Model):
    title = models.CharField(verbose_name="제목", max_length=256)
    is_confirmed = models.BooleanField(verbose_name="계약 확인 여부", default=False)
    manager = models.ForeignKey(
        verbose_name="계약 담당자",
        to=User,
        on_delete=models.DO_NOTHING,
    )
    is_legal_team_confirmed = models.BooleanField(
        verbose_name="법무팀 확인 여부", default=False
    )
    legal_team_manager = models.ForeignKey(
        verbose_name="법무팀 담당자",
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="+",
        null=True,
        blank=True,
    )
    is_finance_team_confirmed = models.BooleanField(
        verbose_name="재무팀 확인 여부", default=False
    )
    finance_team_manager = models.ForeignKey(
        verbose_name="재무팀 담당자",
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="+",
        null=True,
        blank=True,
    )
    is_security_team_confirmed = models.BooleanField(
        verbose_name="보안팀 확인 여부", default=False
    )
    security_team_manager = models.ForeignKey(
        verbose_name="보안팀 담당자",
        to=User,
        on_delete=models.DO_NOTHING,
        related_name="+",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "contract"
        verbose_name = "계약"
        verbose_name_plural = "계약 목록"
