from dataclasses import field
from rest_framework.serializers import ModelSerializer
from experiences.models import Perk, Experience
from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    perks = PerkSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    host = TinyUserSerializer(read_only=True)

    class Meta:
        model = Experience
        fields = (
            "id",
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "start",
            "end",
            "host",
            "category",
            "perks",
        )
