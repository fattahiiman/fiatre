from __future__ import unicode_literals
from zeep import Client

from django.db import models
import requests
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import UserManager
from django.conf import settings

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(_('phone'), max_length=11, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    is_superuser = models.BooleanField(_('is superuser'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    is_watching = models.BooleanField(_('is watching'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['password']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def get_phone(self):
        return self.phone

    def get_subscription(self):
        return self.subscription.filter(status=True).first()

    def sms_reset_password(self, phone, code):
        message = """سلام\n\nکاربر گرامی کد بازیابی رمز عبور شما {0} می باشد.\n\nفیاتر\nwww.fiatre.ir""".format(code)

        data = {
            'username': settings.SMS_USERNAME,
            'password': settings.SMS_PASSWORD,
            'to': phone,
            'from': settings.SMS_FROM_NUMBER,
            'text': message,
        }

        result = requests.post('https://rest.payamak-panel.com/api/SendSMS/SendSMS', data).json()
        if result['RetStatus'] == 1:
            return True
        else:
            return False

    def sms_disposable_code(self , phone, code):
        pass