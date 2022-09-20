from django.contrib import admin

from houses.models import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "address", "pet_allowed"]
    list_filter = ["price", "pet_allowed"]
    search_fields = ["address"]
