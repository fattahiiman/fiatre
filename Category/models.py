from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
import time

def upload_image(instance , filename):
    path = 'categories/' + slugify(instance.name , allow_unicode=True)
    name = str(time.time()) + '-' + str(get_random_string()) + '-' + filename

    return path + '/' + name

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='عنوان')
    slug = models.SlugField(verbose_name='نامک' , allow_unicode=True , unique=True)
    image = models.ImageField(verbose_name='عکس', upload_to=upload_image , null=True)
    description = models.TextField(max_length=500, verbose_name='توضیحات')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name
