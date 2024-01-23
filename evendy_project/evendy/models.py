from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(default='profile_pics/profile_default.jpg', upload_to='profile_pics')
    description = models.TextField(blank=True)
    user_planned_events = models.ManyToManyField('Event', through='UserPlannedEvent')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

    @property
    def calculated_age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return 0


class UserPlannedEvent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    place = models.CharField(max_length=250)
    image = models.ImageField(default='event_pics/event_default.jpg', upload_to='event_pics')
    attendees_looking_for_company = models.ManyToManyField(Profile, related_name='events_who_is_looking_for_company')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

#
# class Invitation(models.Model):
#     sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inv_sender')
#     recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inv_recipient')
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     is_accepted = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)

