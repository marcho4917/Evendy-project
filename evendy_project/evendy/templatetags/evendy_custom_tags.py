from django import template
from evendy.models import EventCouple

register = template.Library()

@register.simple_tag
def couple_exists(user1, user2, event):
    return EventCouple.objects.filter(profiles=(user1, user2), event=event).exists()

