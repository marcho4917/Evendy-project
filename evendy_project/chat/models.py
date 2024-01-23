from django.db import models
from evendy.models import Profile
from django.db.models import SET
from django.contrib.auth.models import AnonymousUser

class Message(models.Model):
    sender = models.ForeignKey(Profile, related_name='sender', on_delete=SET(AnonymousUser.id))
    receiver = models.ForeignKey(Profile, related_name='receiver', on_delete=SET(AnonymousUser.id))
    message = models.TextField()
    sended_at = models.DateTimeField(auto_now_add=True)



class Room(models.Model):
    sender = models.ForeignKey(Profile, related_name='room_sender', on_delete=SET(AnonymousUser.id))
    receiver = models.ForeignKey(Profile, related_name='room_receiver', on_delete=SET(AnonymousUser.id))
    room_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.room_name