from rest_framework import serializers

from wishlists.models import Wishlist
from rooms.serializers import RoomSerializer

class WishListSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = Wishlist
        fields = ("name","rooms")


