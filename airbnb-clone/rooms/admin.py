from django.contrib import admin

from rooms.models import Room, Amenity

@admin.register(Room)
class RoomsAdmin(admin.ModelAdmin):
    pass


@admin.register(Amenity)
class AmenitysAdmin(admin.ModelAdmin):
    pass