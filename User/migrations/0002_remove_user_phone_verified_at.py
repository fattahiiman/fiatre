# Generated by Django 3.2.5 on 2021-07-28 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_verified_at',
        ),
    ]
