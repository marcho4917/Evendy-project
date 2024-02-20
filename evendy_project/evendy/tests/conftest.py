from pytest_factoryboy import register

from evendy.tests.factories import EventFactory, ProfileFactory, UserFactory

register(EventFactory)
register(ProfileFactory)
register(UserFactory)
