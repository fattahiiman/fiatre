# Generated by Django 3.2.2 on 2021-08-02 20:21

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('slug', models.SlugField(verbose_name='نامک')),
                ('time', models.CharField(max_length=50, verbose_name='زمان')),
                ('episode', models.CharField(max_length=50, verbose_name='قسمت')),
                ('teacher', models.CharField(max_length=50, verbose_name='استاد')),
                ('view_count', models.CharField(max_length=50, verbose_name='تعداد بازدید')),
                ('description', models.TextField(max_length=50, verbose_name='توضیحات')),
                ('image', models.ImageField(upload_to='images', verbose_name='عکس')),
                ('video', models.FileField(upload_to='videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])], verbose_name='فیلم')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='Category.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'فیلم',
                'verbose_name_plural': 'فیلم ها',
            },
        ),
    ]
