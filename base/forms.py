from django import forms
from django.contrib.auth.forms import UserCreationForm

from .locations import NigeriaStates
from .models import User


class UserRegistrationForm(UserCreationForm):
    is_service_provider = forms.BooleanField(required=False)
    is_home_owner = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "input-form password-input"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "input-form password-input"}
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "is_service_provider", "is_home_owner")
        exclude = ("username",)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_service_provider = self.cleaned_data["is_service_provider"]
        user.is_home_owner = self.cleaned_data["is_home_owner"]

        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput)


class ServiceProviderProfileForm(forms.Form):
    DAYS_OF_WEEK = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    ]

    provider_name = forms.CharField(
        label="Provider Name", max_length=100, required=True
    )
    phone_number = forms.CharField(label="Phone Number", max_length=100, required=True)
    email = forms.EmailField(label="Email", max_length=100, required=True)
    days_of_week = forms.CharField(label="Days of the Week")
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    state = forms.ChoiceField(
        label="State",
        required=True,
        choices=NigeriaStates.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    hourly_rate = forms.IntegerField(
        label="Hourly Rate", max_value=999_999_999, min_value=100, required=True
    )
    bio = forms.CharField(label="Bio", widget=forms.Textarea, required=True)
