from django.contrib import admin

from rooms.models import Room, Amenity


@admin.action(description="price를 0으로 바꾸기")
def set_price_zero(admin_models, request, rooms):
    for room in rooms:
        room.price = 0
        room.save()


@admin.register(Room)
class RoomsAdmin(admin.ModelAdmin):

    actions = (set_price_zero,)

    list_display = (
        "name",
        "country",
        "city",
        "address",
        "price",
        "total_amenities",
        "rating",
        "rooms",
        "toilets",
        "kind",
        "onwer",
    )

    list_filter = ("amenities",)

    search_fields = (
        "name",
        "=price",
        "^onwer__username",
    )


@admin.register(Amenity)
class AmenitysAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = ("created_at", "updated_at")
