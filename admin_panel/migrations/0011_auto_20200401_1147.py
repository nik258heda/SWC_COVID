# Generated by Django 3.0.3 on 2020-04-01 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0010_auto_20200401_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=300),
        ),
    ]