# Generated by Django 3.2.13 on 2022-09-22 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Amenity',
            new_name='Amenitys',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='amenity',
        ),
        migrations.AddField(
            model_name='rooms',
            name='amenitys',
            field=models.ManyToManyField(to='rooms.Amenitys'),
        ),
    ]