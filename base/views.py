from rest_framework import viewsets

from .models import (
    Homeowner,
    ServiceProvider,
    User,
    TimeSlot,
    Booking,
    Review,
    ProviderAvailability,
)
from .serializers import (
    HomeownerSerializer,
    ServiceProviderSerializer,
    UserSerializer,
    TimeSlotSerializer,
    BookingSerializer,
    ReviewSerializer,
    ProviderAvailabilitySerializer,
)


class HomeownerViewSet(viewsets.ModelViewSet):
    queryset = Homeowner.objects.all()
    serializer_class = HomeownerSerializer


class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ProviderAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = ProviderAvailability.objects.all()
    serializer_class = ProviderAvailabilitySerializer
