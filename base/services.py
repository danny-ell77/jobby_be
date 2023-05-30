import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import models, IntegrityError
from django.db.models import Q

from .models import (
    ServiceProvider,
    Booking,
    Review,
    ProviderAvailability,
    BookingStatus,
    Homeowner,
)

d = models.Model.objects


class ServiceProviderSearchService:
    def search_service_providers(
        self, keyword: str, location: str, hourly_rate: dict, rating: dict
    ) -> List[ServiceProvider]:
        rating_predicate = rating.get("rating_predicate")
        rating_value = rating.get("rating_value")
        rating_lookup = (
            {f"rating__{rating_predicate}": rating_value}
            if rating_predicate and rating_value
            else dict()
        )

        hourly_rate_predicate = hourly_rate.get("hourly_rate_predicate")
        hourly_rate_value = hourly_rate.get("hourly_rate_value")
        hourly_rate_lookup = (
            {f"hourly_rate__{hourly_rate_predicate}": hourly_rate_value}
            if hourly_rate_predicate and hourly_rate_value
            else dict()
        )

        providers = ServiceProvider.objects.filter(
            Q(name__icontains=keyword)
            | Q(location=location)
            | Q(**hourly_rate_lookup)
            | Q(**rating_lookup)
        )
        # We can also filter on availability!
        # We can filter by service type
        # We can filter by Service Area
        return providers

    def get_service_provider_details(
        self, provider_id: int
    ) -> Optional[ServiceProvider]:
        try:
            provider = ServiceProvider.objects.get(id=provider_id)
            return provider
        except ServiceProvider.DoesNotExist:
            return None


class ServiceProviderAvailabilityService:
    def set_availability(self, provider_id: int, availability: dict) -> bool:
        start_time_obj = datetime.strptime(availability["start_time"], "%H:%M").time()
        end_time_obj = datetime.strptime(availability["end_time"], "%H:%M").time()
        if not (start_time_obj > end_time_obj):
            return False
        try:
            provider = ServiceProvider.objects.get(id=provider_id)
            ProviderAvailability.objects.create(
                service_provider=provider,
                start_time=start_time_obj,
                end_time=end_time_obj,
            )
            return True
        except ServiceProvider.DoesNotExist:
            return False
        except IntegrityError:
            return False

    def accept_booking_request(self, booking_id: uuid.UUID) -> bool:
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = BookingStatus.APPROVED
            booking.save()
            return True
        except Booking.DoesNotExist:
            return False

    def reject_booking_request(self, booking_id: uuid.UUID) -> bool:
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = BookingStatus.REJECTED
            booking.save()
            return True
        except ServiceProvider.DoesNotExist:
            return False

    def create_a_booking(self, allotted_time: dict, provider_id: uuid.UUID):
        start_time_obj = datetime.strptime(allotted_time["start_time"], "%H:%M").time()
        end_time_obj = datetime.strptime(allotted_time["end_time"], "%H:%M").time()
        availabilty = ProviderAvailability.objects.get(provider__id=provider_id)
        date = allotted_time["date"]


class ConfirmationReminderService:
    def __init__(self, booking: Booking):
        self.service_provider_name = booking.service_provider.user.get_full_name()
        self.service_provider_email = booking.service_provider.user.email
        self.homeowner__name = booking.homeowner.user.get_full_name()
        self.service_location = booking.homeowner.user.location
        self.difference_in_time = timedelta(datetime.now(), booking.slot.start_time)

    def send_confirmation_message(self) -> bool:
        # Implement logic to send a confirmation message for the appointment
        message = f"""
                <h1>Hi {self.service_provider_name},</h1> 
                This is a subtle reminder about your appointment with 
                {self.homeowner__name} at {self.service_location} in {self.difference_in_time}
                """
        return self._send_email(message)

    def send_reminder_message(self) -> bool:
        # Implement logic to send a reminder message for the appointment, minutes_before indicates the reminder time
        # On the celery task call delay with the time set to 1 hour before the time
        message = f"""
                <h1>Hi {self.homeowner__name},</h1> 
                This is a subtle reminder about your appointment with 
                {self.service_provider_name} at {self.service_location} in {self.difference_in_time}
                """
        return self._send_email(message)

    def _send_email(self, message: str) -> bool:
        try:
            send_mail(
                subject="Appointment Reminder",
                html_message=message,
                message=message,
                from_email="Jobby no-reply@jobby.com",
                recipient_list=[f"{self.service_provider_email}"],
                fail_silently=False,
            )
        except Exception as e:
            return False
        return True


class UpcomingBookingsService:
    def get_upcoming_appointments(self, provider_id: uuid.UUID) -> List[Booking]:
        try:
            upcoming_appointments = Booking.objects.filter(
                service_provider__id=provider_id, slot__start_time__gte=datetime.now()
            )
            return upcoming_appointments
        except ServiceProvider.DoesNotExist:
            return []

    def get_appointment_details(self, booking_id: uuid.UUID) -> Optional[Booking]:
        try:
            appointment = Booking.objects.get(id=booking_id)
            return appointment
        except ObjectDoesNotExist:
            return None

    def cancel_appointment(self, booking_id: uuid.UUID) -> bool:
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = BookingStatus.CANCELLED
            booking.save()
            return True
        except Booking.DoesNotExist:
            return False


class ReviewsFeedbackService:
    def leave_rating_and_feedback(
        self,
        appointment_id: int,
        rating: int,
        feedback: str,
        reviewer_id: uuid.UUID,
        provider_id: uuid.UUID,
    ) -> bool:
        try:
            reviewer = Homeowner.objects.get(id=reviewer_id)
            service_provider = ServiceProvider.objects.get(id=provider_id)
            Review.objects.create(
                comments=feedback,
                rating=rating,
                homeowner=reviewer,
                service_provider=service_provider,
            )
            return True
        except ObjectDoesNotExist:
            return False

    def get_provider_ratings(self, provider_id: uuid.UUID) -> List[Review]:
        try:
            ratings = Review.objects.filter(provider__id=provider_id)
            return ratings
        except ObjectDoesNotExist:
            return []
