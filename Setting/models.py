from django.db import models

class Setting(models.Model):
    key = models.CharField(verbose_name='کلید' , max_length=255 , unique=True)
    value = models.TextField(verbose_name='مقدار')

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'تنظیمات'
        verbose_name_plural = 'تنظیمات ها'

    def __str__(self):
        return self.key