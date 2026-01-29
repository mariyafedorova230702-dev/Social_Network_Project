
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Post, Comment
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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Что нового?",
                "rows": 3
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            })
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        