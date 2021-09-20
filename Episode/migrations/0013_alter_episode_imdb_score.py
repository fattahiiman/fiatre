# Generated by Django 3.2.2 on 2021-08-14 15:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Episode', '0012_alter_episode_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='imdb_score',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.RegexValidator(message='امتیاز imdb باید عددی باشد', regex='^(1[0-2]|[1-9])$')], verbose_name='امتیاز imdb'),
        ),
    ]
