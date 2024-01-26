from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from .models import Notice, Invitation
from evendy.models import Profile, Event
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


class NoticesListView(ListView):
    model = Notice
    template_name = 'notices/notices_list.html'

    def get_queryset(self):
        return Notice.objects.filter(recipient=self.request.user.profile)


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

        content_type = ContentType.objects.get_for_model(Invitation)
        content_id = invitation.id
        message = f'{sender.user.username} want go with you to this event: {event.title}'

        Notice.objects.create(
            recipient=recipient,
            content_type=content_type,
            content_id=content_id,
            content_text=message
        )

        messages.success(request, f"You just send an invitation!")
        return redirect('event_details', event_id)

