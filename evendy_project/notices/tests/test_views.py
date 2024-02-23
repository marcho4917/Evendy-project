import pytest
from django.urls import reverse
from notices.models import Notice, Invitation
from evendy.models import Profile, Event

pytestmark = pytest.mark.django_db


def test_if_notices_list_is_uploaded_to_context(client, django_user_model):
    username = "test-user"
    password = "test-password"
    user = django_user_model.objects.create_user(username=username, password=password)
    profile = Profile.objects.get(user=user)
    client.login(username=username, password=password)

    Notice.objects.create(recipient=profile, content_text='test-text-1')
    Notice.objects.create(recipient=profile, content_text='test-text-2')

    response = client.get('/notices-list/')

    notices_for_user = Notice.objects.filter(recipient=profile)

    assert response.status_code == 200
    assert len(notices_for_user) == 2


def test_if_user_invites_list_is_loaded_to_context(client, django_user_model):
    username = 'recipient'
    password = 'test-password'
    recipient_user = django_user_model.objects.create(username=username, password=password)
    sender_user = django_user_model.objects.create(username='sender')

    recipient_profile = Profile.objects.get(user=recipient_user)
    sender_profile = Profile.objects.get(user=sender_user)

    client.force_login(recipient_user)
    client.force_login(sender_user)

    event1 = Event.objects.create(title='test-event1', date='2024-05-05')
    event2 = Event.objects.create(title='test-event2', date='2024-06-05')

    Invitation.objects.create(sender=sender_profile, recipient=recipient_profile, event=event1)
    Invitation.objects.create(sender=sender_profile, recipient=recipient_profile, event=event2)

    invites_for_user = Invitation.objects.filter(recipient=recipient_profile)

    response = client.get('/invites-list/')

    assert response.status_code == 200
    assert len(invites_for_user) == 2


def test_if_invitation_is_canceled(client, django_user_model):
    username = 'recipient'
    password = 'test-password'
    recipient_user = django_user_model.objects.create(username=username, password=password)
    recipient_profile = Profile.objects.get(user=recipient_user)

    sender_user = django_user_model.objects.create(username='sender')
    sender_profile = Profile.objects.get(user=sender_user)

    client.force_login(recipient_user)
    client.force_login(sender_user)

    event = Event.objects.create(title='test-event', date='2024-05-05')
    invitation = Invitation.objects.create(sender=sender_profile, recipient=recipient_profile, event=event)

    url = reverse('cancel_going_out_together', args=[invitation.id, recipient_profile.id, event.id])

    response = client.post(url)

    assert not Invitation.objects.filter(id=invitation.id).exists()


def test_if_invite_is_created(client, django_user_model):
    username = 'recipient'
    password = 'test-password'
    recipient_user = django_user_model.objects.create(username=username, password=password)
    recipient_profile = Profile.objects.get(user=recipient_user)
    recipient_profile.phone_number = '111111111111'

    sender_user = django_user_model.objects.create(username='sender')
    sender_profile = Profile.objects.get(user=sender_user)
    sender_profile.phone_number = '222222222222'

    client.force_login(recipient_user)
    client.force_login(sender_user)

    print("sender phone number:", sender_profile.phone_number)
    print("recipient phone number:", recipient_profile.phone_number)
    event = Event.objects.create(title='test-event', date='2024-05-05')
    event.attendees_looking_for_company.add(recipient_profile)
    event.attendees_looking_for_company.add(sender_profile)
    print("ATENDEEES:", event.attendees_looking_for_company.all())
    print("ID recipient:", recipient_profile.id)
    url = reverse('send_invite', args=[event.id, recipient_profile.id])

    response = client.post(url)
    print("url:", url)
    print("INVITATIONS:", Invitation.objects.filter(sender=sender_profile.id))
    assert Invitation.objects.filter(sender=sender_profile.id, recipient=recipient_profile.id, event=event.id, is_accepted=False).exists()


def test_if_invitation_is_accepted_correctly(client, django_user_model):
    username = 'recipient'
    password = 'test-password'
    recipient_user = django_user_model.objects.create(username=username, password=password)
    recipient_profile = Profile.objects.get(user=recipient_user)
    recipient_profile.phone_number = '111111111111'

    sender_user = django_user_model.objects.create(username='sender')
    sender_profile = Profile.objects.get(user=sender_user)
    sender_profile.phone_number = '222222222222'

    client.force_login(recipient_user)
    client.force_login(sender_user)

    event = Event.objects.create(title='test-event', date='2024-05-05')
    event.attendees_looking_for_company.add(recipient_profile)
    event.attendees_looking_for_company.add(sender_profile)
    invitation = Invitation.objects.create(sender=sender_profile, recipient=recipient_profile, event=event)

    url = reverse('accept_or_decline_invitation', args=[invitation.id, recipient_profile.id, event.id])

    response = client.post(url, {'action': 'accept'})
    print("INVITATIONS:", Invitation.objects.all())
    assert Invitation.objects.filter(sender=sender_profile.id, recipient=recipient_profile.id, event=event.id, is_accepted=True).exists()


def test_if_invitation_is_decline_correctly(client, django_user_model):
    username = 'recipient'
    password = 'test-password'
    recipient_user = django_user_model.objects.create(username=username, password=password)
    recipient_profile = Profile.objects.get(user=recipient_user)
    recipient_profile.phone_number = '111111111111'

    sender_user = django_user_model.objects.create(username='sender')
    sender_profile = Profile.objects.get(user=sender_user)
    sender_profile.phone_number = '222222222222'

    client.force_login(recipient_user)
    client.force_login(sender_user)

    event = Event.objects.create(title='test-event', date='2024-05-05')
    event.attendees_looking_for_company.add(recipient_profile)
    event.attendees_looking_for_company.add(sender_profile)
    invitation = Invitation.objects.create(sender=sender_profile, recipient=recipient_profile, event=event)

    url = reverse('accept_or_decline_invitation', args=[invitation.id, recipient_profile.id, event.id])

    response = client.post(url, {'action': 'decline'})

    assert not Invitation.objects.filter(sender=sender_profile.id, recipient=recipient_profile.id, event=event.id, is_accepted=True).exists()
