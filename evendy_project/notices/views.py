from django.shortcuts import redirect, render
from .models import Notice, Invitation
from evendy.models import Profile, Event, UserPlannedEvent, EventCouple
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


def notices_list(request):
    notices_for_user = Notice.objects.filter(recipient=request.user.profile)

    notices_for_user.update(is_read=True)

    return render(request, 'notices/notices_list.html', {'notices_for_user': notices_for_user})


def invites_list(request):
    invites_for_user = Invitation.objects.filter(recipient=request.user.profile)

    return render(request, 'notices/user_invites.html', {'invites_for_user': invites_for_user})


def send_invite(request, event_id, profile_id):
    if request.method == 'POST':
        event = Event.objects.get(pk=event_id)
        sender = request.user.profile
        recipient = Profile.objects.get(pk=profile_id)

        check_if_invitation_exists = Invitation.objects.filter(sender=sender, recipient=recipient, event=event).exists()

        if check_if_invitation_exists:
            messages.warning(request, "Invitation already sent!")
        else:
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

            new_event_couple = EventCouple.objects.create(event=event)
            new_event_couple.profiles.add(sender, recipient)
            new_event_couple.save()

            event.attendees_looking_for_company.remove(user_to_delete_from_attendees_looking_for_company)
            event.attendees_looking_for_company.remove(recipient)

            Invitation.objects.filter(sender=sender, event=event).exclude(id=invitation.id).delete()

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

            #send notice
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


def cancel_going_out_together(request, invite_id, profile_id, event_id):
    if request.method == 'POST':
        invitation = Invitation.objects.get(pk=invite_id)
        recipient = Profile.objects.get(pk=profile_id)
        event = Event.objects.get(pk=event_id)
        logged_user = request.user.profile

        event_couple_to_delete = EventCouple.objects.filter(event=event, profiles=logged_user).filter(profiles=recipient)
        event_couple_to_delete.delete()

        # send notice
        content_type = ContentType.objects.get(app_label="notices", model="invitation")
        content_id = invitation.id
        message = f'Sorry, but {request.user.profile}, cancel going out with you to: {event.title}'

        Notice.objects.create(
            recipient=recipient,
            content_type=content_type,
            content_id=content_id,
            content_text=message
        )

        invitation.delete()

        event.attendees_looking_for_company.add(recipient)

    return redirect('invites_list')

