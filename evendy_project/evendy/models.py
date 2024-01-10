from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=250)
    image = models.ImageField(default='event_default.jpg', upload_to='event_pics')
    # attends_looking_for_company = models.ManyToManyField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(default='profile_default.jpg', upload_to='profile_pics')
    user_planned_events = models.ManyToManyField(Event, through='UserPlannedEvent')
    #user_friends_from_events =

    @property
    def calculated_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return 0


class UserPlannedEvent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
