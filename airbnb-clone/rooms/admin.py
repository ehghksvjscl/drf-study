from django.contrib import admin

from rooms.models import Room, Amenity


@admin.register(Room)
class RoomsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "city",
        "address",
        "price",
        "rooms",
        "toilets",
        "kind",
        "onwer",
    )

    list_filter = ("amenitys",)


@admin.register(Amenity)
class AmenitysAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = ("created_at", "updated_at")
