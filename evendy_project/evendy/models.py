from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=250)
    image = models.ImageField(default='event_default.jpg', upload_to='event_pics')
    attends_looking_for_company =


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth =
    description = models.TextField()
    profile_image = models.ImageField(default='profile_default.jpg', upload_to='profile_pics')
    user_planned_events =
    user_friends_from_events =

    def calculate_age(self):
        pass

