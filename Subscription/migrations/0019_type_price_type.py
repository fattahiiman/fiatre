# Generated by Django 3.2.2 on 2021-12-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Subscription', '0018_auto_20211202_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='price_type',
            field=models.CharField(choices=[('UD', 'دلار'), ('TM', 'تومان')], default='TM', max_length=2, verbose_name='نوع ارز'),
        ),
    ]
