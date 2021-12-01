from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify
import time
from Category.models import Category
from utils.models import CustomModel


def upload_image(instance , filename):
    path = 'episodes/images/' + slugify(instance.title , allow_unicode=True)
    name = str(time.time()) + '-' + str(get_random_string()) + '-' + filename

    return path + '/' + name


def upload_video(instance , filename):
    path = 'episodes/videos/' + slugify(instance.title , allow_unicode=True)
    name = str(time.time()) + '-' + str(get_random_string()) + '-' + filename

    return path + '/' + name


class Episode(CustomModel):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    slug = models.SlugField(verbose_name='نامک' , allow_unicode=True , unique=True)
    time = models.IntegerField(verbose_name='زمان')
    episode = models.CharField(verbose_name='قسمت' , max_length=255 , null=True , blank=True)
    teacher = models.CharField(max_length=100, verbose_name='استاد' , null=True , blank=True)
    view_count = models.IntegerField(default=0 , verbose_name='تعداد بازدید' , null=True , blank=True)
    description = models.TextField(verbose_name='توضیحات')
    imdb_score = models.FloatField(default=0.0 , verbose_name='امتیاز imdb' , null=True , blank=True)
    genre = models.CharField(max_length=100, verbose_name='ژانر' , null=True , blank=True)
    director = models.CharField(max_length=100, verbose_name='کارگردان' , null=True , blank=True)
    writer = models.CharField(max_length=100, verbose_name='نویسنده' , null=True , blank=True)
    actors = models.CharField(max_length=255, verbose_name='بازیگران' , null=True , blank=True)
    country = models.CharField(max_length=100, verbose_name='محصول کشور' , null=True , blank=True)
    construction_year = models.CharField(max_length=100, verbose_name='سال ساخت' , null=True , blank=True)

    TYPE_OPTIONS = (('educational', 'آموزشی'), ('movie', 'فیلم'))
    type = models.CharField(max_length=11, choices=TYPE_OPTIONS, verbose_name='نوع' , default='movie')

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='episodes',
                                 verbose_name='دسته بندی')

    image = models.ImageField(verbose_name='عکس', upload_to=upload_image)

    video = models.TextField(verbose_name='لینک دانلود (mp4)' , null=True , blank=True)

    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم ها'

    def __str__(self):
        return self.title


    def get_video_mp4_url(self):
        return self.video