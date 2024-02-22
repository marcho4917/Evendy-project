import pytest
from evendy.models import Event, UserPlannedEvent, Profile


pytestmark = pytest.mark.django_db


def test_if_register_form_is_render(client):
    response = client.get('/register/')

    assert response.status_code == 200


def test_if_profile_view_is_render_with_authenticated_client(client, django_user_model):
    username = "test-user"
    password = "test-password"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    response = client.get('/profile/')

    assert response.status_code == 200


def test_if_event_details_view_is_render(client):
    event = Event.objects.create(title='test-event', date='2024-06-06')
    response = client.get('/event-details/1/')

    assert response.status_code == 200


def test_if_user_planned_events_are_correctly_added_to_context(client, django_user_model):
    username = "test-user"
    password = "test-password"
    user = django_user_model.objects.create_user(username=username, password=password)
    profile = Profile.objects.get(user=user)
    client.login(username=username, password=password)

    event = Event.objects.create(title='test-event', date='2024-06-06')
    UserPlannedEvent.objects.create(profile=profile, event=event)

    response = client.get('/my-events/')

    assert response.status_code == 200


