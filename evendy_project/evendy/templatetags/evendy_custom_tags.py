from django import template
from notices.models import Invitation, Notice

register = template.Library()


@register.filter
def has_unread_notif(user):
    notifications = Notice.objects.filter(recipient=user, is_read=False)
    if notifications.exists():
        return True
    return False
