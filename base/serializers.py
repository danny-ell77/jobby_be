from rest_framework import serializers
from .models import (
    Homeowner,
    ServiceProvider,
    ServiceType,
    ServiceArea,
    User,
    TimeSlot,
    Booking,
    Review,
    ProviderAvailability,
)


class HomeownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homeowner
        fields = ("id", "user")


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = ("id", "user", "bio", "rating", "hourly_rate", "location")


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ("id", "name", "description")


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ("id", "name", "description")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "is_service_provider")


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ("id", "start_time", "end_time", "is_booked")


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "slot",
            "homeowner",
            "service_provider",
            "payment_amount",
            "payment_status",
            "status",
        )


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "homeowner", "service_provider", "rating", "comments")


class ProviderAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderAvailability
        fields = (
            "id",
            "service_provider",
            "days_of_the_week",
            "start_time",
            "end_time",
        )
