# store/forms.py

from django import forms
from django.contrib.auth.models import (
    User,
)  # Change depending on whether you're using a custom User model


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User  # or your custom User model
        fields = ["username", "first_name", "last_name", "email", "password"]


# Make sure SignUpForm is defined below, like so:
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User  # or your custom User model
        fields = ["username", "email", "password"]
