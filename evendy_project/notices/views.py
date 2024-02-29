from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .models import Notice, Invitation
from evendy.models import Profile, Event, UserPlannedEvent, EventCouple
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages


def notices_list(request):
    notices_for_user = Notice.objects.filter(recipient=request.user.profile).order_by('-created_at')

    notices_for_user.update(is_read=True)

    paginator = Paginator(notices_for_user, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notices/notices_list.html', {'page_obj': page_obj})


def invites_list(request):
    invites_for_user = Invitation.objects.filter(recipient=request.user.profile)
    invites_sent_from_user = Invitation.objects.filter(sender=request.user.profile)

    return render(request, 'notices/user_invites.html', {'invites_for_user': invites_for_user, 'invites_sent_from_user': invites_sent_from_user})


def send_invite(request, event_id, profile_id):
    if request.method == 'POST':
        event = Event.objects.get(pk=event_id)
        sender = request.user.profile
        recipient = Profile.objects.get(pk=profile_id)

        if Invitation.objects.filter(sender=sender, event=event, is_accepted=True).exists() or \
                Invitation.objects.filter(recipient=sender, event=event, is_accepted=True).exists():
            messages.error(request, "You have already buddy for this event!")
        elif Invitation.objects.filter(sender=sender, recipient=recipient, event=event).exists():
            messages.error(request, "Invitation already sent!")
        elif Invitation.objects.filter(recipient=sender, sender=recipient, event=event).exists():
            messages.warning(request, 'This user also sent you an invitation to this event, accept it in "My Invites"')
        elif not sender.phone_number:
            messages.warning(request, 'If yot want to send invitation, you have to add youre phone number first')
        elif sender not in event.attendees_looking_for_company.all():
            messages.warning(request, 'If you want to send invitations you have to be signed in this event')
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

            messages.success(request, f"You just sent an invitation!")
    return redirect('event_details', event_id)


def accept_or_decline_invitation(request, invite_id, profile_id, event_id):
    if request.method == 'POST':
        invitation = Invitation.objects.get(pk=invite_id)
        action = request.POST.get('action')
        sender = Profile.objects.get(pk=profile_id)
        event = Event.objects.get(pk=event_id)
        logged_user_and_recipient = request.user.profile

        if action == 'accept':
            invitation.is_accepted = True
            invitation.save()

            new_event_couple = EventCouple.objects.create(event=event)
            new_event_couple.profiles.add(sender, logged_user_and_recipient)
            new_event_couple.save()

            event.attendees_looking_for_company.remove(logged_user_and_recipient)
            event.attendees_looking_for_company.remove(sender)

            Invitation.objects.filter(sender=sender, event=event, is_accepted=False).delete()
            Invitation.objects.filter(event=event, sender=request.user.profile, is_accepted=False).exclude(id=invitation.id).delete()
            Invitation.objects.filter(recipient=request.user.profile, event=event).exclude(id=invitation.id).delete()

            logged_user_and_recipient.user_planned_events.remove(event)
            sender.user_planned_events.remove(event)
            content_type = ContentType.objects.get(app_label="notices", model="invitation")
            content_id = invitation.id
            message = f'{request.user.profile}, accepted your invitation to: {event.title}, visit profile to see contact details'

            Notice.objects.create(
                recipient=sender,
                content_type=content_type,
                content_id=content_id,
                content_text=message
            )

        elif action == 'decline':
            invitation.is_canceled = True
            invitation.delete()

            #send notice
            content_type = ContentType.objects.get(app_label="notices", model="invitation")
            content_id = invitation.id
            message = f'{request.user.profile}, decline your invitation to: {event.title}'

            Notice.objects.create(
                recipient=sender,
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

        event_couple_to_delete = EventCouple.objects.filter(event=event, profiles__in=[recipient, logged_user])
        event_couple_to_delete.delete()

        # send notice
        content_type = ContentType.objects.get(app_label="notices", model="invitation")
        content_id = invitation.id
        message = f'Sorry, but {request.user.profile}, canceled going out with you to: {event.title}'

        Notice.objects.create(
            recipient=recipient,
            content_type=content_type,
            content_id=content_id,
            content_text=message
        )

        event.attendees_looking_for_company.add(recipient)
        event.attendees_looking_for_company.add(logged_user)

        recipient.user_planned_events.add(event)
        logged_user.user_planned_events.add(event)

        invitation.delete()

    return redirect('invites_list')

