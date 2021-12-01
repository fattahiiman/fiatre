from django.db import models
from django.contrib.auth import get_user_model
from utils.models import CustomModel

User = get_user_model()

class PasswordReset(CustomModel):
    code = models.CharField(verbose_name='کد' , max_length=5)
    user = models.ForeignKey(verbose_name='کاربر' ,to=User , on_delete=models.CASCADE , related_name='password_resets')
    is_used = models.BooleanField(verbose_name='آیا استفاده شده است' , default=False)

    class Meta:
        verbose_name = 'بازیابی رمز عبور'
        verbose_name_plural = 'بازیابی رمز عبور ها'

    def __str__(self):
        return self.user.phone


class LoginCode(CustomModel):
    code = models.CharField(verbose_name='کد' , max_length=5)
    user = models.ForeignKey(verbose_name='کاربر' ,to=User , on_delete=models.CASCADE , related_name='login_codes')
    is_used = models.BooleanField(verbose_name='آیا استفاده شده است' , default=False)

    created_at = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='تاریخ ویرایش', auto_now=True)

    class Meta:
        verbose_name = 'کد یکبار مصرف ورود'
        verbose_name_plural = 'کد ها یکبار مصرف ورود'

    def __str__(self):
        return f"{self.user.phone}-{self.code}"