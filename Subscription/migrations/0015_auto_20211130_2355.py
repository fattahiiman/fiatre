# Generated by Django 3.2.2 on 2021-11-30 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Subscription', '0014_auto_20211130_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='updated_at',
        ),
    ]