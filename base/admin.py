from django.contrib import admin

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


@admin.register(Homeowner)
class HomeownerAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "is_service_provider",
        "is_home_owner",
    )
    list_filter = [
        "email",
        "is_service_provider",
        "is_home_owner",
    ]
    search_fields = [
        "email",
        "is_service_provider",
        "is_home_owner",
    ]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(ProviderAvailability)
class ProviderAvailabilityAdmin(admin.ModelAdmin):
    pass
