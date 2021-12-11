from django.db import models
from utils.models import CustomModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Coupon(CustomModel):
    code = models.CharField(max_length=255 , verbose_name='کد' , unique=True)
    time = models.IntegerField(default=1 , verbose_name='مدت زمان استفاده (ماه)')
    percent = models.IntegerField(verbose_name='درصد تخفیف')

    TYPE_OPTIONS = (('UD', 'دلار'), ('TM', 'تومان'))
    type = models.CharField(max_length=2, choices=TYPE_OPTIONS, verbose_name='نوع', default='TM')

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد تخفیف های تخفیف'

    def __str__(self):
        return self.code + '-' + str(self.time) + 'ماهه'


class CouponUser(CustomModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='used_coupons',verbose_name='کاربر')
    coupon = models.ForeignKey(to=Coupon, on_delete=models.CASCADE, related_name='used_coupons',verbose_name='کد تخفیف')

    class Meta:
        verbose_name = 'کد تخفیف استفاده شده'
        verbose_name_plural = 'کد تخفیف های تخفیف استفاده شده'

    def __str__(self):
        return f"{self.user}-{self.coupon.code}"