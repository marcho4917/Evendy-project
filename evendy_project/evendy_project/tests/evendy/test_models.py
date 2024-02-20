import pytest

pytestmark = pytest.mark.django_db


class TestEventModel:
    def test_should_return_correct_event_title_as_string(self, event_factory):
        event = event_factory(title='test-event-title')
        assert event.__str__() == 'test-event-title'


class TestUserModel:
    def test_should_return_correct_username_as_string(self, user_factory):
        user = user_factory(username='test-username')
        assert user.__str__() == 'test-username'
