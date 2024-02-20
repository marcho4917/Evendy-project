from datetime import date

import factory.django
from django.contrib.auth.models import User
from evendy.models import Event, Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'test_username'


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = 'test_event'
    date = date.today()
    # time =
    place = 'test_place'





