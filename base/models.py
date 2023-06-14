import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.managers import UserManager


class DaysOfTheWeek(models.IntegerChoices):
    """
    Enumeration representing the days of the week.
    """

    MONDAY = 1, "Monday"
    TUESDAY = 2, "Tuesday"
    WEDNESDAY = 3, "Wednesday"
    THURSDAY = 4, "Thursday"
    FRIDAY = 5, "Friday"
    SATURDAY = 6, "Saturday"
    SUNDAY = 7, "Sunday"


class BookingStatus(models.TextChoices):
    """
    Enumeration representing the status of a booking.
    """

    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"


class BookingPaymentStatus(models.TextChoices):
    """
    Enumeration representing the payment status of a booking.
    """

    SUCCESSFUL = "SUCCESSFUL"
    PENDING = "PENDING"
    FAILED = "FAILED"


class UUIDPrimaryKey(models.Model):
    """
    Abstract base model providing a UUID primary key field.
    """

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
    """
    Abstract base model providing fields for tracking object history.
    """

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
    """
    Model representing a homeowner.
    """

    user = models.OneToOneField("User", on_delete=models.CASCADE)

    def __str__(self):
        """
        Return a string representation of the homeowner.
        """
        return f"Homeowner: {self.user.email}"


class ServiceProvider(UUIDPrimaryKey, ObjectHistoryTracker):
    """
    Model representing a service provider.
    """

    user = models.OneToOneField("User", on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    hourly_rate = models.DecimalField(
        verbose_name="hourly rate", max_digits=8, decimal_places=2
    )
    availability = models.ForeignKey(
        "ProviderAvailability",
        on_delete=models.CASCADE,
        related_name="service_providers",
        blank=True,
        null=True,
    )
    service_type = models.ForeignKey(
        "ServiceType",
        on_delete=models.CASCADE,
        related_name="service_providers",
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("?",)

    def __str__(self):
        """
        Return a string representation of the service provider.
        """
        return self.provider_name


class ServiceType(UUIDPrimaryKey, ObjectHistoryTracker):
    """
    Model representing a service type.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        """
        Return a string representation of the service type.
        """
        return self.name


class ServiceArea(UUIDPrimaryKey, ObjectHistoryTracker):
    """
    Model representing a service area.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        """
        Return a string representation of the service area.
        """
        return self.name


class User(UUIDPrimaryKey, AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """

    username = None
    email = models.EmailField(
        verbose_name=_("email address"), blank=False, null=False, unique=True
    )
    is_service_provider = models.BooleanField(
        verbose_name=_("is service provider"), default=False
    )
    is_home_owner = models.BooleanField(verbose_name=_("is home owner"), default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """
        Return a string representation of the user.
        """
        return self.email


class TimeSlot(UUIDPrimaryKey, ObjectHistoryTracker):
    """
    Model representing a time slot.
    """

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField()


class Booking(UUIDPrimaryKey, ObjectHistoryTracker):
    """
    Model representing a booking.
    """

    slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    homeowner = models.ForeignKey(Homeowner, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(
        choices=BookingPaymentStatus.choices, max_length=255
    )
    status = models.CharField(max_length=255, choices=BookingStatus.choices)

    def __str__(self):
        """
        Return a string representation of the booking.
        """
        return f"Booking for {self.service_provider.provider_name} by {self.homeowner.user.email}"


class Review(UUIDPrimaryKey, ObjectHistoryTracker):
    """
    Model representing a review.
    """

    homeowner = models.ForeignKey(
        Homeowner, on_delete=models.CASCADE, related_name="reviews"
    )
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comments = models.TextField()

    def __str__(self):
        """
        Return a string representation of the review.
        """
        return f"Review for {self.service_provider.provider_name} by {self.homeowner.user.email}"


class ProviderAvailability(UUIDPrimaryKey, ObjectHistoryTracker):
    """
    Model representing the availability of a service provider.
    """

    days_of_the_week = models.CharField(max_length=500, blank=True, null=True)
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
        verbose_name="End Time",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="start_time_before_end_time",
                violation_error_message="Start time must be before end time.",
            ),
        ]
        verbose_name_plural = "Provider availabilities"

    def __str__(self):
        """
        Return a string representation of the provider availability.
        """
        return f"{self.start_time} to {self.end_time} on {self.days_of_the_week}"
