from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password', 'gender']

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['priority']