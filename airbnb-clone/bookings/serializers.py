from rest_framework import serializers

from django.utils import timezone

from bookings.models import Booking


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )


class CreateBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    def validate_check_in(self, data):
        if timezone.localdate(timezone.now()) > data:
            raise serializers.ValidationError("Can't book in the past!")

        return data

    def validate_check_out(self, data):
        if timezone.localdate(timezone.now()) > data:
            raise serializers.ValidationError("Can't book in the past!")

        return data

    def validate(self, data):
        if data["check_in"] >= data["check_out"]:
            raise serializers.ValidationError("체크인 날짜는 체크아웃 날짜 보다 크면 안됩니다.")

        room_pk = self.context["request"].parser_context["kwargs"]["pk"]

        if Booking.objects.filter(
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
            room=room_pk,
        ).exists():
            raise serializers.ValidationError("이미 예약이 있습니다.")

        return data

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )
