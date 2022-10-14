from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomSerializer


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
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            return Response(RoomSerializer(room).data)
        else:
            return Response(serializer.errors)
