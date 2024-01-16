from django.contrib.auth.forms import UserCreationForm, User
from django import forms
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'date_of_birth']


class ProfileUpdateForm(forms.ModelForm):
    description = forms.TextInput()

    class Meta:
        model = Profile
        fields = ['profile_image', 'description']
