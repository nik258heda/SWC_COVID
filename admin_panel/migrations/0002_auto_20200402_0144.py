# Generated by Django 3.0.3 on 2020-04-02 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='v_const',
            field=models.IntegerField(default=2),
        ),
    ]