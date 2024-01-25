from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Event, Profile, UserPlannedEvent
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Dear {username}, you have been successfully signed up!")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'evendy/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile been updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'evendy/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class EventDetailsView(DetailView):
    model = Event
    template_name = 'evendy/event_details.html'


class EventListView(ListView):
    model = Event
    template_name = 'evendy_api/evendy_api.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["now"] = timezone.now()
    #     return context


def add_or_remove_user_from_seekers(request, event_id):
    if request.method == 'POST':
        event = Event.objects.get(pk=event_id)
        action = request.POST.get('action')

        if request.user.is_authenticated:
            if action == 'add':
                UserPlannedEvent.objects.create(profile=request.user.profile, event=event)
                event.attendees_looking_for_company.add(request.user.profile)
                messages.success(request, f"Congrats, now just wait for your buddy!")
            elif action == 'remove':
                UserPlannedEvent.objects.filter(profile=request.user.profile, event=event).delete()
                event.attendees_looking_for_company.remove(request.user.profile)
                messages.success(request, f"You are no longer looking for a buddy for this event")
        else:
            messages.warning(request, "You have to be logged in.")

    return redirect('event_details', pk=event_id)


def search_events(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        events = Event.objects.filter(title__contains=searched)
        return render(request, 'evendy/search_events.html', {'searched': searched, 'events': events})


def profile_details(request, user_id):
    profile = Profile.objects.get(user=user_id)

    return render(request, 'evendy/profile_details.html', {'profile': profile})


def show_my_events(request):
    user_profile = request.user.profile
    planned_events = user_profile.user_planned_events.all()

    return render(request, 'evendy/user_events.html', {'planned_events': planned_events})

