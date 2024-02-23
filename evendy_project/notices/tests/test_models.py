import pytest
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from notices.models import Notice, Invitation
from evendy.models import Profile, Event

pytestmark = pytest.mark.django_db


def test_if_invitation_is_created_correctly():
    user1 = User.objects.create(username='sender')
    user2 = User.objects.create(username='recipient')

    sender_profile = Profile.objects.get(user=user1)
    recipient_profile = Profile.objects.get(user=user2)

    event = Event.objects.create(title='test-event', date='2024-05-05')

    invitation = Invitation.objects.create(sender=sender_profile, recipient=recipient_profile, event=event)

    assert invitation.sender == sender_profile
    assert invitation.recipient == recipient_profile
    assert invitation.event == event
    assert invitation.is_accepted == False


def test_if_notice_is_created_correctly():
    user = User.objects.create(username='recipient')
    recipient_profile = Profile.objects.get(user=user)

    content_type = ContentType.objects.create(model='test')
    content_id = 1
    content_text = 'notice-test'

    notice = Notice.objects.create(content_type=content_type, content_id=content_id, content_text=content_text, recipient=recipient_profile)

    assert notice.recipient == recipient_profile
    assert notice.content_text == 'notice-test'

