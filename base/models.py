import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class DaysOfTheWeek(models.IntegerChoices):
    MONDAY = 1, "Monday"
    TUESDAY = 2, "Tuesday"
    WEDNESDAY = 3, "Wednesday"
    THURSDAY = 4, "Thursday"
    FRIDAY = 5, "Friday"
    SATURDAY = 6, "Saturday"
    SUNDAY = 7, "Sunday"


class BookingStatus(models.TextChoices):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"


class BookingPaymentStatus(models.TextChoices):
    SUCCESSFUL = "SUCCESSFUL"
    PENDING = "PENDING"
    FAILED = "FAILED"


class UUIDPrimaryKey(models.Model):
    id = models.UUIDField(
        verbose_name="id",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("UUID primary key"),
    )

    class Meta:
        abstract = True


class ObjectHistoryTracker(models.Model):

    created_at = models.DateTimeField(
        verbose_name=_("creation date"),
        editable=False,
        auto_now_add=True,
    )
    created_by = models.UUIDField(
        verbose_name=_("created by"),
        editable=False,
        null=True,
    )
    last_modified_at = models.DateTimeField(
        verbose_name=_("last modified date"),
        editable=False,
        auto_now=True,
    )
    last_modified_by = models.UUIDField(
        verbose_name=_("last modified by"),
        null=True,
        editable=False,
    )

    class Meta:
        abstract = True


class Homeowner(UUIDPrimaryKey, ObjectHistoryTracker):
    user = models.OneToOneField("User", on_delete=models.CASCADE)


class ServiceProvider(UUIDPrimaryKey, ObjectHistoryTracker):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    bio = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True)
    hourly_rate = models.DecimalField(
        verbose_name="hourly rate", max_digits=8, decimal_places=2
    )
    location = models.CharField(max_length=255)


class ServiceType(UUIDPrimaryKey, ObjectHistoryTracker):
    name = models.CharField(max_length=255)
    description = models.TextField()


class ServiceArea(UUIDPrimaryKey, ObjectHistoryTracker):
    name = models.CharField(max_length=255)
    description = models.TextField()


class User(AbstractUser):
    is_service_provider = models.BooleanField(default=False)


class TimeSlot(UUIDPrimaryKey, ObjectHistoryTracker):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField()


class Booking(UUIDPrimaryKey, ObjectHistoryTracker):
    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(
        choices=BookingPaymentStatus.choices, max_length=255
    )
    status = models.CharField(max_length=255, choices=BookingStatus.choices)


class Review(UUIDPrimaryKey, ObjectHistoryTracker):
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comments = models.TextField()


class ProviderAvailability(UUIDPrimaryKey, ObjectHistoryTracker):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    days_of_the_week = ArrayField(
        base_field=models.IntegerField(choices=DaysOfTheWeek.choices), size=7
    )

    start_time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        help_text="Format: HH:MM (24-hour)",
        verbose_name="Start Time",
    )

    end_time = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        help_text="Format: HH:MM (24-hour)",
        verbose_name="Start Time",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="start_time_before_end_time",
                violation_error_message="Start time must be before end time.",
            ),
        ]
