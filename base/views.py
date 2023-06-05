from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from base.forms import UserRegistrationForm, AuthenticationForm


class RegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "base/registration.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, "base/registration.html", {"form": form})


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
