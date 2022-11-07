from . import models
from strawberry.types import Info


def get_all_rooms(info: Info):
    return models.Room.objects.all().select_related("owner").prefetch_related("reviews")


def get_room(pk: int):
    try:
        return models.Room.objects.get(pk=pk)
    except models.Room.DoesNotExist:
        return None


def create_room(info: Info):
    pass
