# Generated by Django 3.2.2 on 2021-08-01 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_remove_user_phone_verified_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='phone'),
        ),
    ]
