# Generated by Django 3.2.12 on 2022-10-12 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.CharField(choices=[('FINANCE_TEAM', '재무팀'), ('SECURITY_TECH_TEAM', '보안기술팀'), ('SECURITY_TEAM', '보안팀'), ('LEGAL_TEAM', '법무팀'), ('NO_TEAM', '팀없음')], max_length=50),
        ),
    ]
