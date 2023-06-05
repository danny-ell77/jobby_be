from django import forms
from django.contrib.auth.forms import UserCreationForm

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
