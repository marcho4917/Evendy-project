import pytest
from django.urls import reverse
from evendy.models import Event, UserPlannedEvent, Profile


pytestmark = pytest.mark.django_db


def test_if_register_form_is_render(client):
    response = client.get('/register/')

    assert response.status_code == 200


def test_if_profile_view_is_render_with_authenticated_client(client, django_user_model):
    user = django_user_model.objects.create_user(username='test-user', password='test-password')
    client.force_login(user)
    response = client.get('/profile/')

    assert response.status_code == 200


def test_if_event_details_view_is_render(client):
    Event.objects.create(title='test-event', date='2024-06-06')
    response = client.get('/event-details/1/')

    assert response.status_code == 200


def test_if_user_planned_events_are_correctly_added_to_context(client, django_user_model):
    user = django_user_model.objects.create_user(username='test-user', password='test-password')
    client.force_login(user)

    event = Event.objects.create(title='test-event', date='2024-06-06')
    UserPlannedEvent.objects.create(profile=user.profile, event=event)

    url = reverse('add_or_remove_user_from_seekers', args=[event.id])

    response = client.get('/my-events/')
    response_with_action = client.post(url, {'action': 'add'})

    assert UserPlannedEvent.objects.filter(profile=user.profile, event=event).exists()
    assert response.status_code == 200


def test_if_user_planned_events_are_correctly_removed_from_context(client, django_user_model):
    user = django_user_model.objects.create_user(username='test-user', password='test-password')
    client.force_login(user)

    event = Event.objects.create(title='test-event', date='2024-06-06')
    UserPlannedEvent.objects.create(profile=user.profile, event=event)

    url = reverse('add_or_remove_user_from_seekers', args=[event.id])

    response = client.get('/my-events/')
    response_with_action = client.post(url, {'action': 'remove'})

    assert not UserPlannedEvent.objects.filter(profile=user.profile, event=event).exists()
    assert response.status_code == 200