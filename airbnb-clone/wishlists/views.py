from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from wishlists.models import Wishlist
from  wishlists.serializers import WishListSerializer

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

