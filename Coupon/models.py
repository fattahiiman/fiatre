from django.db import models
from utils.models import CustomModel


class Coupon(CustomModel):
    code = models.CharField(max_length=255 , verbose_name='کد' , unique=True)
    time = models.IntegerField(default=1 , verbose_name='مدت زمان استفاده (ماه)')
    percent = models.IntegerField(verbose_name='درصد تخفیف')

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد تخفیف های تخفیف'

    def __str__(self):
        return self.code + '-' + str(self.time) + 'ماهه'