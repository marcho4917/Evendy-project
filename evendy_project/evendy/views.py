from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import Event, Profile
from django.views.generic.list import ListView


def evendy_home(request):
    return render(request, 'evendy/events_list.html', {'events': Event.objects.all()}) #do wyswietlania kart z eventami na stronie glownej


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'evendy/register.html', {'form': form})


def profile(request):
    return render(request, 'evendy/profile.html')


def event_details(request):
    return render(request, 'evendy/event_details.html')


class EventListView(ListView):
    model = Event
    template_name = 'evendy/events_list.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["now"] = timezone.now()
    #     return context