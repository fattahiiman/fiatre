from django.db import models
from utils.models import CustomModel

class Setting(CustomModel):
    key = models.CharField(verbose_name='کلید' , max_length=255 , unique=True)
    value = models.TextField(verbose_name='مقدار')

    class Meta:
        verbose_name = 'تنظیمات'
        verbose_name_plural = 'تنظیمات ها'

    def __str__(self):
        return self.key