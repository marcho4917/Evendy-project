# Generated by Django 5.0.1 on 2024-01-26 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evendy', '0008_delete_invitation'),
        ('notices', '0003_rename_verb_notice_content_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notice_recipient', to='evendy.profile'),
        ),
    ]