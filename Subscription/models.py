from django.db import models
from django.contrib.auth import get_user_model
from utils.models import CustomModel

User = get_user_model()

class Type(CustomModel):
    name = models.CharField(max_length=50, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, verbose_name='نامک' , allow_unicode=True , unique=True)
    time = models.PositiveBigIntegerField(verbose_name='مدت زمان' , unique=True)
    price = models.PositiveBigIntegerField(verbose_name='قیمت')

    TYPE_OPTIONS = (('full', 'کامل'), ('view', 'فقط تماشا'))
    type = models.CharField(max_length=11, choices=TYPE_OPTIONS, verbose_name='نوع اشتراک' , default='movie')

    class Meta:
        verbose_name = 'اشتراک'
        verbose_name_plural = 'اشتراک ها'

    def __str__(self):
        return self.name + '-' + f"{self.time} ماهه"


    def get_type(self):
        return self.type


class Subscription(CustomModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscription', verbose_name='کاربر')
    type = models.ForeignKey(to=Type, on_delete=models.CASCADE, related_name='users', verbose_name='نوع اشتراک')

    status = models.BooleanField(verbose_name='وضعیت' , default=False , null=True , blank=True)

    class Meta:
        verbose_name = 'اشتراک کاربران'
        verbose_name_plural = 'اشتراک های کاربران'

    def __str__(self):
        return self.user.phone + '-' + self.type.name