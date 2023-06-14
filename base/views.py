"""
This module contains the implementation of various Django views
that handle different user interactions and render the appropriate templates.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from base.forms import (
    UserRegistrationForm,
    AuthenticationForm,
    ServiceProviderProfileForm,
    ProviderSearchForm,
    ProviderFilterForm,
)
from base.models import ServiceProvider, ProviderAvailability, ServiceType


class RegistrationView(View):
    """This view handles user registration."""

    def get(self, request):
        """
        Renders the registration form.
        :param request: The HTTP request object.
        :return:  The rendered registration form template.
        """
        form = UserRegistrationForm()
        return render(request, "base/registration.html", {"form": form})

    def post(self, request):
        """
        :param request: The HTTP request object.
        :return: Redirects the user to the appropriate page after successful registration,
        or renders the registration form template with errors if the form is invalid.
        """
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if form.data["is_service_provider"]:
                return redirect("service_provider_profile")
            return redirect("login")
        return render(request, "base/registration.html", {"form": form})


class ServiceProviderProfileView(View):
    """This view handles the creation and update of service provider profiles."""

    def get(self, request):
        """
        Renders the service provider profile form.
        :param request: The HTTP request object.
        :return:  The rendered service provider profile form template.
        """
        form = ServiceProviderProfileForm()
        return render(request, "base/service_provider_profile.html", {"form": form})

    def post(self, request):
        """
        Handles the service provider profile form submission.
        :param request: The HTTP request object.
        :return: Redirects the provider to the homepage
        """
        form = ServiceProviderProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            p = ProviderAvailability.objects.create(
                days_of_the_week=data["days_of_week"],
                start_time=data["start_time"],
                end_time=data["end_time"],
            )
            ServiceProvider.objects.create(
                user=request.user,
                availability=p,
                bio=data["bio"],
                hourly_rate=data["hourly_rate"],
                provider_name=data["provider_name"],
                location=data["state"],
            )
        return redirect("home")


class LoginView(View):
    """This view handles user authentication and login."""

    def get(self, request):
        """
        Renders the login form.
        :param request: The HTTP request object.
        :return: The rendered login form template.
        """
        form = AuthenticationForm()
        return render(request, "base/login.html", {"form": form})

    def post(self, request):
        """
        Handles the login form submission.
        :param request: The HTTP request object.
        :return: Redirects the user to the home page after successful login,
        or renders the login form template with errors if the credentials are invalid.
        """
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            remember_me = request.POST.get("remember_me")
            user = authenticate(username=username, password=password)
            if user is not None:
                if remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(None)
                login(request, user)
                return redirect("home")

        messages.error(request, message="Invalid email or password")
        return render(request, "base/login.html", {"form": form})


class HomeView(View):
    """This view handles the rendering of the home page and search/filter functionality."""

    def get(self, request):
        """
        Renders the home page.
        :param request: The HTTP request object.
        :return: The rendered home page template
        """
        if request.user and request.user.is_service_provider:
            return render(request, "base/service_provider_home.html")
        qs = ServiceProvider.objects.filter(is_active=True)
        context = {
            "search_form": ProviderSearchForm(),
            "filter_form": ProviderFilterForm(),
            "locations": qs.values_list("location", flat=True).distinct(),
            "service_providers": qs,
            "qs_count": qs.count(),
        }
        return render(request, "base/home.html", context)

    def post(self, request, action):
        """
        Handles form submissions on the home page.
        :param request: The HTTP request object.
        :param action: The action to be performed (e.g., "search" or "filter").
        :return: The result of the specified action method.
        """
        action = getattr(self, action)
        return action(request)

    def search(self, request):
        """
        Handles the search form submission.
        :param: request: The HTTP Request object
        :return: The rendered home page template with the search results
        """
        form = ProviderSearchForm(data=request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_query"]
            location = form.cleaned_data["location"]
            qs = ServiceProvider.objects.filter(
                Q(location__icontains=location)
                & (
                    Q(service_type__name__exact=query)
                    | Q(provider_name__icontains=query)
                )
            )
            context = {
                "service_providers": qs,
                "qs_count": qs.count(),
                "search_form": form,
                "filter_form": ProviderFilterForm(),
            }
            return render(request, "base/home.html", context)

    def filter(self, request):
        """
        Handles the filter form submission.
        :param request: The HTTP Request object
        :return The rendered home page template with filtered search results.
        """
        form = ProviderFilterForm(data=request.POST)
        context = {
            "search_form": ProviderSearchForm(),
            "filter_form": form,
        }
        if form.is_valid():
            location = form.cleaned_data["location"]
            service_type = form.cleaned_data["service_type"]
            ratings = form.cleaned_data["ratings"]
            availability = form.cleaned_data["availability"]
            if availability == "weekends":
                availability_query = Q()
                for day in ["Saturday", "Sunday"]:
                    availability_query |= Q(
                        availability__days_of_the_week__contains=day
                    )
            elif availability == "weekdays":
                availability_query = Q()
                for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                    availability_query |= Q(
                        availability__days_of_the_week__contains=day
                    )
            else:
                availability_query = Q(
                    availability__days_of_the_week__contains=availability
                )
            query = Q()
            if location:
                query &= Q(location=location)
            if service_type:
                query &= Q(service_type__name__exact=service_type)
            if ratings:
                query &= Q(rating=int(ratings))
            if availability:
                query &= availability_query
            qs = ServiceProvider.objects.filter(query)
            context["service_providers"] = qs
            context["qs_count"] = qs.count()
            return render(request, "base/home.html", context)
        return render(request, "base/home.html", context)


@method_decorator(login_required, name="dispatch")
class ServiceProviderDetail(View):
    """This view handles the rendering of the service provider details page."""

    def get(self, request, pk):
        """
        Renders the service provider details page.
        :param request: The HTTP request object.
        :param pk: The primary key of the service provider.
        :returns: The rendered service provider details template.
        """
        provider = ServiceProvider.objects.get(id=pk)
        context = {
            "provider": provider,
            "related_providers": ServiceProvider.objects.filter(
                Q(service_type__name=provider.service_type.name),
            ),
        }
        return render(request, "base/service_provider_details.html", context)


class ServiceTypeList(View):
    """This view handles the rendering of the list of service providers for a specific service type."""

    def get(self, request, service_type):
        """
        Renders the list of service providers for a specific service type.
        :param request: The HTTP request object.`
        :param service_type: The name of the service type.
        :return: The rendered service type list template.
        """
        qs = ServiceProvider.objects.filter(service_type__name=service_type)
        context = {"service_providers": qs, "qs_count": qs.count()}
        return render(request, "base/service_type_list.html", context)


class LandingView(View):
    """This view handles the rendering of the landing page."""

    def get(self, request):
        """
        Renders the landing page.
        :param request:The HTTP request object.
        :return: he rendered landing page template.
        """
        context = {
            "search_form": ProviderSearchForm(),
            "services": ServiceType.objects.all().prefetch_related("service_providers")[
                :10
            ],
            "service_providers": ServiceProvider.objects.filter(rating=5),
        }
        return render(request, "base/landing.html", context)
