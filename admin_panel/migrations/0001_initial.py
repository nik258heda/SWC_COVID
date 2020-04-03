# Generated by Django 3.0.3 on 2020-04-03 10:17

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('requirement', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('address_allowed', models.BooleanField(default=True)),
                ('timestamp_for_id', models.BigIntegerField(default=0)),
                ('user_remarks', models.TextField(blank=True, max_length=1024)),
                ('admin_remarks', models.TextField(blank=True, max_length=1024)),
                ('status_completed', models.BooleanField(default=False)),
                ('v_const', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='admin_panel.Category')),
                ('requestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL)),
                ('urgency_rating', models.ManyToManyField(blank=True, related_name='post_urgency', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('timestamp_for_id', models.BigIntegerField(default=0)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.Request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
