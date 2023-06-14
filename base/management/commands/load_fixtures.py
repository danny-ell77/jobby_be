import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from base.mock_data import search_results, generate_password, generate_time_fields
from base.models import (
    ServiceType,
    ProviderAvailability,
    ServiceProvider,
    User,
    Review,
    Homeowner,
)
from base.users import users_list


class Command(BaseCommand):
    """
    Django management command to populate the database with generated data.
    """

    help = "Populate db with generated data"

    def handle(self, *args, **options):
        """
        Handle method to populate the database with generated data.
        """
        for user_det, service_provider in zip(users_list[:51], search_results):
            print(f"Processing user: {user_det}")
            user = self.create_user_from_details(user_det)
            self.create_or_get_service_type(service_provider)
            p = self.create_provider_availability(service_provider)
            service_provider__ = self.create_service_provider(user, p, service_provider)

            for review in service_provider["reviews"]:
                user__ = self.create_user_from_review(review)
                homeowner = self.create_homeowner(user__)
                self.create_review(homeowner, service_provider__, review)

    def create_user_from_details(self, user_det):
        """
        Create a user from the details provided.

        :param user_det: User details.
        :type user_det: dict
        :return: Created user object.
        :rtype: User
        """
        first_name, last_name = user_det["name"].split(" ")
        return User.objects.create_user(
            user_det["email"],
            password=generate_password(),
            first_name=first_name,
            last_name=last_name,
            is_service_provider=True,
            is_home_owner=False,
        )

    def create_or_get_service_type(self, service_provider):
        """
        Create or get the service type.

        :param service_provider: Service provider details.
        :type service_provider: dict
        :return: Created or retrieved service type object.
        :rtype: ServiceType
        """
        name = service_provider["serviceType"]
        return ServiceType.objects.get_or_create(name=name)

    def create_provider_availability(self, service_provider):
        """
        Create provider availability.

        :param service_provider: Service provider details.
        :type service_provider: dict
        :return: Created provider availability object.
        :rtype: ProviderAvailability
        """
        start_time, end_time = generate_time_fields(
            service_provider["availabilityTime"]
        )
        return ProviderAvailability.objects.create(
            days_of_the_week=service_provider["daysAvailable"],
            start_time=start_time,
            end_time=end_time,
        )

    def create_service_provider(self, user, availability, service_provider):
        """
        Create a service provider.

        :param user: User object.
        :type user: User
        :param availability: Provider availability object.
        :type availability: ProviderAvailability
        :param service_provider: Service provider details.
        :type service_provider: dict
        :return: Created service provider object.
        :rtype: ServiceProvider
        """
        s = service_provider["serviceType"]
        return ServiceProvider.objects.create(
            user=user,
            availability=availability,
            bio=service_provider["aboutCompany"],
            provider_name=service_provider["company"],
            service_type=s,
            hourly_rate=random.randint(200, 1_000_000),
            rating=random.randint(1, 5),
            location=service_provider["location"],
        )

    def create_user_from_review(self, review):
        """
        Create a user from the review details.

        :param review: Review details.
        :type review: dict
        :return: Created user object.
        :rtype: User
        """
        first_name, last_name = review["reviewer"].split(" ")
        try:
            return User.objects.create_user(
                review["email"],
                password=generate_password(),
                first_name=first_name,
                last_name=last_name,
            )
        except IntegrityError:
            random_number = random.randint(1, 9999)
            modified_email = review["email"].replace("@", f"_{random_number}@")
            return User.objects.create_user(
                email=modified_email,
                password=generate_password(),
                first_name=first_name,
                last_name=last_name,
            )

    def create_homeowner(self, user):
        """
        Create a homeowner.

        :param user: User object.
        :type user: User
        :return: Created homeowner object.
        :rtype: Homeowner
        """
        return Homeowner.objects.create(user=user)

    def create_review(self, homeowner, service_provider, review):
        """
        Create a review.

        :param homeowner: Homeowner object.
        :type homeowner: Homeowner
        :param service_provider: Service provider object.
        :type service_provider: ServiceProvider
        :param review: Review details.
        :type review: dict
        :return: Created review object.
        :rtype: Review
        """
        return Review.objects.create(
            homeowner=homeowner,
            service_provider=service_provider,
            rating=review["rating"],
            comments=review["comment"],
        )
