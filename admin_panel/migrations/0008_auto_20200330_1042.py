# Generated by Django 3.0.3 on 2020-03-30 10:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_panel', '0007_auto_20200330_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='urgency_rating',
        ),
        migrations.AddField(
            model_name='request',
            name='urgency_rating',
            field=models.ManyToManyField(blank=True, related_name='post_urgency', to=settings.AUTH_USER_MODEL),
        ),
    ]
