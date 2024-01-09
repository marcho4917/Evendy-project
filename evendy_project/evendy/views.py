from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import Event


def home(request):
    return render(request, 'evendy/events.html', {'events': Event.objects.all()})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'evendy/register.html', {'form': form})


def profile():
    pass


def login():
    pass