from django.urls import path

from base.views import (
    RegistrationView,
    LoginView,
    ServiceProviderProfileView,
    HomeView,
    ServiceProviderDetail,
    ServiceTypeList,
    LandingView,
)

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path(
        "provider-profile",
        ServiceProviderProfileView.as_view(),
        name="service_provider_profile",
    ),
    path("home", HomeView.as_view(), name="home"),
    path("home/<str:action>", HomeView.as_view(), name="home"),
    path(
        "provider/<uuid:pk>",
        ServiceProviderDetail.as_view(),
        name="service_provider_detail",
    ),
    path(
        "providers/<str:service_type>",
        ServiceTypeList.as_view(),
        name="service_type_list",
    ),
]
