# Generated by Django 5.0.1 on 2024-01-10 08:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('place', models.CharField(max_length=250)),
                ('image', models.ImageField(default='event_default.jpg', upload_to='event_pics')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField()),
                ('profile_image', models.ImageField(default='profile_default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlannedEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evendy.event')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evendy.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='user_planned_events',
            field=models.ManyToManyField(through='evendy.UserPlannedEvent', to='evendy.event'),
        ),
    ]