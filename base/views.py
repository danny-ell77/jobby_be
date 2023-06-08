from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from base.forms import (
    UserRegistrationForm,
    AuthenticationForm,
    ServiceProviderProfileForm,
)
from base.models import ServiceProvider, ProviderAvailability


class RegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "base/registration.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            if form.data["is_service_provider"]:
                return redirect("service_provider_profile")
            return redirect("login")
        return render(request, "base/registration.html", {"form": form})


class ServiceProviderProfileView(View):
    def get(self, request):
        form = ServiceProviderProfileForm()
        return render(request, "base/service_provider_profile.html", {"form": form})

    def post(self, request):
        print(request.POST)
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


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "base/login.html", {"form": form})

    def post(self, request):
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
    def get(self, request):
        if request.user.is_home_owner:
            return render(request, "base/home.html")

        return render(request, "base/service_provider_home.html")
