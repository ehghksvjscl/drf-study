from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, ParseError

from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomSerializer, RoomDetailSerializer
from rooms.decorator import room_auth_check
from categories.models import Category
from categories.crud import get_category_or_400

# Amenities
class Amenities(APIView):
    def get(self, request):
        amenities = Amenity.objects.all()
        serializer = AmenitySerializer(amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Amenity, pk=pk)

    def get(self, request, pk: int):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk: int):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk: int):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Room
class Rooms(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():

                # Category
                category = get_category_or_400(request.data.get("category"))

                try:
                    # Start transction
                    with transaction.atomic():

                        # Room
                        room = serializer.save(owner=request.user, category=category)

                        # Amenities
                        amenities = request.data.get("amenities")
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)
                except Exception:
                    raise ParseError("Amenity not found")

                return Response(RoomDetailSerializer(room).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk: int):
        return get_object_or_404(Room, pk=pk)

    def get(self, request, pk: int):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)

    @room_auth_check
    def put(self, request, pk: int):
        room = request.room
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():

            # Category
            category = get_category_or_400(
                request.data.get("category", room.category_id)
            )

            # updated_room = serializer.save()
            # return Response(RoomDetailSerializer(updated_room).data)
            print(category)
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors)

    @room_auth_check
    def delete(self, request, pk: int):
        request.room.delete()
        return Response(status.HTTP_204_NO_CONTENT)
