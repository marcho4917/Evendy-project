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
    # 1 invitation received
    # 2 invite accepted
    # 3 invite declined
#     content_type =  ContentType.object.get(app_label='evendy.Event')
#     content_id = 2
#     content_object = self.content_type.objects.get(id=2)
#     message =  TextField()
#     created_at = models.DateTimeField(default=timezone.now)


