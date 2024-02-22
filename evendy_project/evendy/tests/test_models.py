from datetime import datetime
import pytest
from django.contrib.auth.models import User
from evendy.models import Profile, Event

pytestmark = pytest.mark.django_db


def test_check_if_event_is_created_correctly():
    event = Event.objects.create(title='test-event', date='2024-05-05')

    assert event.__str__() == 'test-event'
    assert event.date == '2024-05-05'


def test_check_if_user_age_is_calculated_correctly_when_date_of_birth_is_correct():
    user = User.objects.create(username='test-user')
    profile = Profile.objects.get(user=user)
    date_of_birth = datetime.strptime('1993-02-13', '%Y-%m-%d').date()

    profile.date_of_birth = date_of_birth

    assert profile.calculated_age == 31


def test_check_if_calculated_age_equals_0_when_date_of_birth_equals_none():
    user = User.objects.create(username='test-user')
    profile = Profile.objects.get(user=user)
    profile.date_of_birth = None

    assert profile.calculated_age == 0


def test_check_if_default_image_is_added_for_profile_when_none_is_loaded():
    user = User.objects.create(username='test-user')
    profile = Profile.objects.get(user=user)

    assert profile.profile_image == 'profile_pics/profile_default.jpg'
