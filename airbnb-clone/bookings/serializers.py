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
        
    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        ) 