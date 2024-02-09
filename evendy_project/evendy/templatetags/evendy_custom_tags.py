from django import template
from notices.models import Invitation

register = template.Library()


@register.simple_tag
def invite_exists(user1, user2, event):
    return Invitation.objects.filter(sender=user1, recipient=user2, event=event).exists()


@register.filter
def invite_exists_2(invitations, sender, event):
    return invitations.objects.filter(sender=sender, event=event).exists()
