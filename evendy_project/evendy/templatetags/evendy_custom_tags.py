from django import template
from evendy.models import EventCouple

register = template.Library()


def couple_exists(sender, recipient, event):
    couple_exists = EventCouple.objects.filter(profiles=(sender, recipient), event=event).exists()

    return couple_exists

