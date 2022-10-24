from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from wishlists.models import Wishlist
from wishlists.serializers import WishListSerializer
from rooms.models import Room

# Wishlist
class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishListSerializer(wishlist, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = WishListSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            return Response(WishListSerializer(wishlist).data)
        else:
            return Response(serializer.errors)

# WishlistDetail
class WishlistDetail(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Wishlist, pk=pk, user=user)

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishListSerializer(wishlist, context={'request':request})
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishListSerializer(wishlist, data=request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            wishlist = serializer.save()
            return Response(WishListSerializer(wishlist).data)
        else:
            return Response(serializer.errors)


class WishlistRoomToggle(APIView):

    permission_classes = [IsAuthenticated]

    def get_wishlist(self, pk, user):
        return get_object_or_404(Wishlist, pk=pk, user=user)

    def get_room(self, room_pk):
        return get_object_or_404(Room, pk=room_pk)
        
    def put(self, request, pk, room_pk):
        wishlist = self.get_wishlist(pk, request.user)
        room = self.get_room(room_pk)

        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return Response(status=status.HTTP_200_OK)