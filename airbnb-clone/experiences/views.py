from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import experiences

from experiences.crud import create_experience_category
from experiences.models import Perk, Experience
from experiences.serializers import PerkSerializer, ExperienceSerializer
from bookings.models import Booking
from bookings.serializers import (
    PublicBookingSerializer,
    CreateExperienceBookingSerializer,
)


class Experiences(APIView):
    """
    GET : List all experiences
    POST : create a new experience.
    """

    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            experience = create_experience_category(request, serializer)
            return Response(
                ExperienceSerializer(experience).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExperienceDetail(APIView):
    """
    GET : get experience detail
    PUT : update experience
    DELETE : delete experience
    """

    def get_object(self, pk: int):
        return get_object_or_404(Experience, pk=pk)

    def get(self, request, pk: int):
        experience = self.get_object(pk)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk: int):
        experience = self.get_object(pk)
        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            experience = create_experience_category(request, serializer)
            return Response(ExperienceSerializer(experience).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk: int):
        experience = self.get_object(pk)
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Bookings(APIView):
    """
    GET : List all bookings
    POST : create a new booking.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_experience(self, pk: int):
        return get_object_or_404(Experience, pk=pk)

    def get(self, request, pk: int):
        experience = self.get_experience(pk)
        bookings = Booking.objects.filter(experience=experience)
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk: int):
        experience = self.get_experience(pk)
        serializer = CreateExperienceBookingSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            booking = serializer.save(user=request.user, experience=experience)
            return Response(
                PublicBookingSerializer(booking).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDetail(APIView):
    """
    GET : get booking detail
    PUT : update booking
    DELETE : delete booking
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_experience(self, pk: int):
        return get_object_or_404(Experience, pk=pk)

    def get_booking(self, booking_pk: int, experience: Experience):
        return get_object_or_404(Booking, pk=booking_pk, experience=experience)

    def get(self, request, pk: int, booking_pk: int):
        experience = self.get_experience(pk)
        booking = self.get_booking(booking_pk, experience)
        serializer = PublicBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk: int, booking_pk: int):
        experience = self.get_experience(pk)
        booking = self.get_booking(booking_pk, experience)
        serializer = PublicBookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk: int, booking_pk: int):
        experience = self.get_experience(pk)
        booking = self.get_booking(booking_pk, experience)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Perks(APIView):
    """
    GET : List all perks
    POST : create a new perk.
    """

    def get(self, request):
        perk = Perk.objects.all()
        serializer = PerkSerializer(perk, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    """
    GET : get perk detail
    PUT : update perk
    DELETE : delete perk
    """

    def get_object(self, pk):
        return get_object_or_404(Perk, pk=pk)

    def get(self, request, pk: int):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk: int):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk: int):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
