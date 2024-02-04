from django import template
from evendy.models import EventCouple

register = template.Library()


def couple_exists(sender, recipient, event):
    couple_to_check = EventCouple.objects.filter(profiles=(sender, recipient), event=event).exists()

    return couple_to_check

