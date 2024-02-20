from pytest_factoryboy import register

from .factories import EventFactory, ProfileFactory, UserFactory

register(EventFactory)
register(ProfileFactory)
register(UserFactory)
