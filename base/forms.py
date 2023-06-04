from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    is_service_provider = forms.BooleanField(required=True)
    is_home_owner = forms.BooleanField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("is_service_provider", "is_home_owner")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_service_provider = self.cleaned_data["is_service_provider"]
        user.is_home_owner = self.cleaned_data["is_home_owner"]

        if commit:
            user.save()
        return user
