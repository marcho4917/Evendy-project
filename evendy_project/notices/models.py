from django.utils import timezone
from django.db import models
from evendy.models import Profile, Event


class Invitation(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inv_sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inv_recipient')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class Notice(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notice_sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notice_recipient')
    verb = models.TextField()
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)