from multiprocessing import context
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.conf import settings

from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomSerializer, RoomDetailSerializer
from rooms.decorator import room_owner_check
from rooms.crud import create_room_amenites_or_category
from categories.crud import get_category_or_400
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer

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

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():

            # Category
            category = get_category_or_400(request.data.get("category"))

            # Amenity
            room = create_room_amenites_or_category(request, serializer, category)

            return Response(RoomDetailSerializer(room).data)
        else:
            return Response(serializer.errors)


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk: int):
        return get_object_or_404(Room, pk=pk)

    def get(self, request, pk: int):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    @room_owner_check
    def put(self, request, pk: int):
        room = request.room
        serializer = RoomDetailSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():

            # Category
            category_pk = request.data.get("category", room.category_id)
            category = get_category_or_400(category_pk)

            # Amenity
            room = create_room_amenites_or_category(request, serializer, category)

            return Response(RoomDetailSerializer(room).data)

        else:
            return Response(serializer.errors)

    @room_owner_check
    def delete(self, request, pk: int):
        request.room.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk: int):
        return get_object_or_404(Room, pk=pk)

    def get(self, request, pk):
        room = self.get_object(pk)

        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = page * page_size

        serializer = ReviewSerializer(room.reviews.all()[start:end], many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, room=room)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomAmenities(APIView):
    def get_object(self, pk: int):
        return get_object_or_404(Room, pk=pk)

    def get(self, request, pk):
        room = self.get_object(pk)

        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = page * page_size

        serializer = AmenitySerializer(room.amenities.all()[start:end], many=True)
        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Room, pk=pk)

    @room_owner_check
    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Room, pk=pk)

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localdate(timezone.now())
        bookings = Booking.objects.filter(
            room__pk=room.pk, kind=Booking.BookingKindChoices.ROOM, check_in__gt=now
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            booking = serializer.save(
                kind=Booking.BookingKindChoices.ROOM,
                user=request.user,
                room=room,
            )
            return Response(PublicBookingSerializer(booking).data)
        else:
            return Response(serializer.errors)
