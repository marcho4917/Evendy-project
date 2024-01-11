from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import Event
from django.views.generic.list import ListView


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'evendy/register.html', {'form': form})


@login_required
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