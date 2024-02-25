import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from notices.models import Notice, Invitation
from evendy.models import Profile, Event

pytestmark = pytest.mark.django_db


def test_if_notices_list_is_uploaded_to_context(client, django_user_model):
    user = django_user_model.objects.create_user(username='test-user', password='test-password')
    client.login(username='test-user', password='test-password')
    Notice.objects.create(recipient=user.profile, content_text='test-text-1')
    Notice.objects.create(recipient=user.profile, content_text='test-text-2')

    response = client.get('/notices-list/')

    notices_for_user = Notice.objects.filter(recipient=user.profile)

    assert response.status_code == 200
    assert len(notices_for_user) == 2


def test_if_invitation_is_canceled(client, django_user_model):
    recipient_user = django_user_model.objects.create_user(username='test-recipient', password='test-password')
    sender_user = django_user_model.objects.create_user(username='test-sender', password='test-password')

    client.force_login(recipient_user)
    client.force_login(sender_user)

    event = Event.objects.create(title='test-event', date='2024-05-05')
    invitation = Invitation.objects.create(recipient=recipient_user.profile, sender=sender_user.profile,  event=event)

    url = reverse('cancel_going_out_together', args=[invitation.id, recipient_user.id, event.id])

    response = client.post(url)

    assert not Invitation.objects.filter(id=invitation.id).exists()


def test_if_invite_is_created(client, django_user_model):
    recipient_user = django_user_model.objects.create_user(username='test-recipient', password='test-password')
    sender_user = django_user_model.objects.create_user(username='test-sender', password='test-password')

    recipient_user.profile.phone_number = '111111111111'
    sender_user.profile.phone_number = '222222222222'

    client.force_login(recipient_user)
    client.force_login(sender_user)

    event = Event.objects.create(title='test-event', date='2024-05-05')
    event.attendees_looking_for_company.add(recipient_user.profile)
    event.attendees_looking_for_company.add(sender_user.profile)

    url = reverse('send_invite', args=[event.id, recipient_user.profile.id])

    response = client.post(url)

    assert Invitation.objects.filter(sender=sender_user.profile.id, recipient=recipient_user.profile.id, event=event.id, is_accepted=False).exists()


def test_if_invitation_is_accepted_correctly(client, django_user_model):
    recipient_user = django_user_model.objects.create_user(username='test-recipient', password='test-password')
    sender_user = django_user_model.objects.create_user(username='test-sender', password='test-password')

    client.force_login(recipient_user)
    client.force_login(sender_user)

    event = Event.objects.create(title='test-event', date='2024-05-05')
    event.attendees_looking_for_company.add(recipient_user.profile)
    event.attendees_looking_for_company.add(sender_user.profile)

    invitation = Invitation.objects.create(sender=sender_user.profile, recipient=recipient_user.profile, event=event)

    url = reverse('accept_or_decline_invitation', args=[invitation.id, recipient_user.profile.id, event.id])

    response = client.post(url, {'action': 'accept'})

    assert Invitation.objects.filter(sender=sender_user.profile.id, recipient=recipient_user.profile.id, event=event.id, is_accepted=True).exists()


def test_if_invitation_is_decline_correctly(client, django_user_model):
    recipient_user = django_user_model.objects.create_user(username='test-recipient', password='test-password')
    sender_user = django_user_model.objects.create_user(username='test-sender', password='test-password')

    client.force_login(recipient_user)
    client.force_login(sender_user)

    event = Event.objects.create(title='test-event', date='2024-05-05')
    event.attendees_looking_for_company.add(recipient_user.profile)
    event.attendees_looking_for_company.add(sender_user.profile)
    invitation = Invitation.objects.create(sender=sender_user.profile, recipient=recipient_user.profile, event=event)

    url = reverse('accept_or_decline_invitation', args=[invitation.id, recipient_user.profile.id, event.id])

    response = client.post(url, {'action': 'decline'})

    assert not Invitation.objects.filter(sender=sender_user.profile.id, recipient=recipient_user.profile.id, event=event.id, is_accepted=True).exists()
