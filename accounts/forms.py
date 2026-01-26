from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.forms import DateInput

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'city', 'birthdate', 'avatar', 'bio']
        widgets = {
            'birthdate': DateInput(attrs={'type': 'date'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'city', 'birthdate', 'avatar', 'bio', 'website']
        widgets = {
            'birthdate': DateInput(attrs={'type': 'date'}),
        }
