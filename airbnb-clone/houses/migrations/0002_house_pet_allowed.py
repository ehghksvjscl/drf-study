# Generated by Django 4.1.1 on 2022-09-07 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='pet_allowed',
            field=models.BooleanField(default=True),
        ),
    ]