# Generated by Django 3.2.13 on 2022-09-04 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recipe_ingredient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='Ingredient',
            new_name='ingredients',
        ),
    ]
