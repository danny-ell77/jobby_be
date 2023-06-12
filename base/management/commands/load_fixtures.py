import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from base.fixtures import search_results, generate_password, generate_time_fields
from base.models import (
    ServiceType,
    ProviderAvailability,
    ServiceProvider,
    User,
    Review,
    Homeowner,
)
from base.sime_users import users_list


class Command(BaseCommand):
    help = "Populate db with generated data"

    def handle(self, *args, **options):
        for user_det, service_provider in zip(users_list[:51], search_results):
            print(user_det)
            some_user = User.objects.create_user(
                user_det["email"],
                password=generate_password(),
                first_name=user_det["name"].split(" ")[0],
                last_name=user_det["name"].split(" ")[1],
                is_service_provider=True,
                is_home_owner=False,
            )
            s, _ = ServiceType.objects.get_or_create(
                name=service_provider["serviceType"]
            )
            start_time, end_time = generate_time_fields(
                service_provider["availabilityTime"]
            )
            p = ProviderAvailability.objects.create(
                days_of_the_week=service_provider["daysAvailable"],
                start_time=start_time,
                end_time=end_time,
            )
            service_provider__ = ServiceProvider.objects.create(
                user=some_user,
                availability=p,
                bio=service_provider["aboutCompany"],
                provider_name=service_provider["company"],
                service_type=s,
                hourly_rate=random.randint(200, 1_000_000),
                rating=random.randint(1, 5),
                location=service_provider["location"],
            )
            for review in service_provider["reviews"]:

                # Attempt to create the user

                try:
                    user__ = User.objects.create_user(
                        review["email"],
                        password=generate_password(),
                        first_name=review["reviewer"].split(" ")[0],
                        last_name=review["reviewer"].split(" ")[1],
                    )
                except IntegrityError:  # Email already exists
                    # Generate a random number
                    random_number = random.randint(1, 9999)
                    some_email = review["email"]
                    # Modify the email by inserting the random number before the @ symbol
                    modified_email = some_email.replace("@", f"_{random_number}@")

                    # Retry creating the user with the modified email
                    user__ = User.objects.create_user(
                        email=modified_email,
                        password=generate_password(),
                        first_name=review["reviewer"].split(" ")[0],
                        last_name=review["reviewer"].split(" ")[1],
                    )
                homeowner = Homeowner.objects.create(user=user__)
                Review.objects.create(
                    homeowner=homeowner,
                    service_provider=service_provider__,
                    rating=review["rating"],
                    comments=review["comment"],
                )
