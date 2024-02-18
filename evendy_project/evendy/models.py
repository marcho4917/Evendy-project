from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(default='profile_pics/profile_default.jpg', upload_to='profile_pics')
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13)
    user_planned_events = models.ManyToManyField('Event', through='UserPlannedEvent')
    user_notices = models.ManyToManyField('notices.Notice', related_name='user_notices', blank=True)
    user_invitations = models.ManyToManyField('notices.Invitation', related_name='user_invitations', blank=True)

    def __str__(self):
        return f'{self.user}'

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
    time = models.TimeField(null=True)
    place = models.CharField(max_length=250)
    image = models.URLField(default='event_pics/event_default.jpg')
    attendees_looking_for_company = models.ManyToManyField(Profile, related_name='events_who_is_looking_for_company')

    def __str__(self):
        return f'{self.title}'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)


class EventCouple(models.Model):
    profiles = models.ManyToManyField(Profile)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def clean(self):
        if self.profiles.count() != 2:
            raise ValidationError('You can relate only 2 profiles')
