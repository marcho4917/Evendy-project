from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.db import models
from evendy.models import Profile, Event
from django.contrib.contenttypes.models import ContentType


class Invitation(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inv_sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inv_recipient')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)


class Notice(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_id')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


