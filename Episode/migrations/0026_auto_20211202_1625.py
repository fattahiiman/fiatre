# Generated by Django 3.2.2 on 2021-12-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Episode', '0025_auto_20211202_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش'),
        ),
    ]
