from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username","password1","password2",]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('ip_address',)
        widgets = {'ip_address':forms.HiddenInput()}

