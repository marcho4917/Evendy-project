from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from .models import Notice, Invitation
from evendy.models import Profile, Event, UserPlannedEvent, EventCouple
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

        # event_couple = EventCouple.objects.create(event=event)

        # event_couple.profiles.add(sender, recipient)

        invitation = Invitation.objects.create(
                sender=sender,
                recipient=recipient,
                event=event
            )

        content_type = ContentType.objects.get(app_label="notices", model="invitation")
        content_id = invitation.id
        message = f'{sender.user.username} sent you invitation to: {event.title}'

        Notice.objects.create(
                recipient=recipient,
                content_type=content_type,
                content_id=content_id,
                content_text=message
            )

        messages.success(request, f"You just send an invitation!")
    return redirect('event_details', event_id)


def accept_or_decline_invitation(request, invite_id, profile_id, event_id):
    if request.method == 'POST':
        invitation = Invitation.objects.get(pk=invite_id)
        action = request.POST.get('action')
        recipient = Profile.objects.get(pk=profile_id)
        event = Event.objects.get(pk=event_id)
        user_to_delete_from_attendees_looking_for_company = request.user.profile

        if action == 'accept':
            invitation.is_accepted = True
            invitation.save()
            sender = invitation.sender


            event.attendees_looking_for_company.remove(user_to_delete_from_attendees_looking_for_company)

            Invitation.objects.filter(sender=sender, event=event).exclude(id=invitation).delete()

            event_couple = EventCouple.objects.create(event=event)
            event_couple.profiles.add(sender, recipient)
            # event_couple.profiles.set([sender, recipient])

            user_to_delete_from_attendees_looking_for_company.user_planned_events.remove(event)
            content_type = ContentType.objects.get(app_label="notices", model="invitation")
            content_id = invitation.id
            message = f'{request.user.profile}, accept your invitation to: {event.title}'

            Notice.objects.create(
                recipient=recipient,
                content_type=content_type,
                content_id=content_id,
                content_text=message
            )

        elif action == 'decline':
            invitation.delete()

            #send notice to invitation sender
            content_type = ContentType.objects.get(app_label="notices", model="invitation")
            content_id = invitation.id
            message = f'{request.user.profile}, decline your invitation to: {event.title}'

            Notice.objects.create(
                recipient=recipient,
                content_type=content_type,
                content_id=content_id,
                content_text=message
            )

    return redirect('invites_list')



