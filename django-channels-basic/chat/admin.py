from django.contrib import admin
from chat.models import Room, RoomMember

admin.site.register(Room)
admin.site.register(RoomMember)