from django.shortcuts import redirect
from django.views.generic.list import ListView
from .models import Notice, Invitation
from evendy.models import Profile, Event


class NoticesListView(ListView):
    model = Notice
    template_name = 'notices/notices_list.html'


class InvitesListView(ListView):
    model = Invitation
    template_name = 'notices/user_invites.html'

    def get_queryset(self):
        return Invitation.objects.filter(recipient=self.request.user.profile)


def send_invite(request, event_id, profile_id):
    if request.method == 'POST':
        event = Event.objects.get(pk=event_id)
        sender = request.user.profile
        recipient = Profile.objects.get(pk=profile_id)

        invitation = Invitation.objects.create(
            sender=sender,
            recipient=recipient,
            event=event
        )

        return redirect('event_details', event_id)

