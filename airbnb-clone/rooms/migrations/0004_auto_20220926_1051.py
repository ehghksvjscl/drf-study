# Generated by Django 3.2.13 on 2022-09-26 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_auto_20220922_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='name',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='amenity',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
