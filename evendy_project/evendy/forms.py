from django.contrib.auth.forms import UserCreationForm, User
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    date_of_birth = forms.DateField()

    class Meta:
        model = User
        fields = ['username', 'email', 'date_of_birth', 'password1', 'password2']
