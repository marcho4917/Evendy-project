from django.contrib.auth.forms import UserCreationForm, User
from django import forms
from .models import Profile
import phonenumbers


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    description = forms.TextInput()
    phone_number = forms.CharField(max_length=12, help_text='Correct phone format: 0xxxxxxxxxx')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Profile
        fields = ['profile_image', 'description', 'phone_number', 'date_of_birth']
