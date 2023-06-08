from django.urls import path

from base.views import RegistrationView, LoginView, ServiceProviderProfileView, HomeView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "provider-profile/",
        ServiceProviderProfileView.as_view(),
        name="service_provider_profile",
    ),
    path("home", HomeView.as_view(), name="home_view"),
]
