from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.models import Q

from User.helpers import check_user_exist

User = get_user_model()

class UserForm(forms.Form):
    phone = forms.CharField(max_length=255, min_length=255, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="شماره موبایل باید عددی باشد",
    )])
    password = forms.CharField(max_length=100 , min_length=8 , required=False)
    password2 = forms.CharField(max_length=100 ,  min_length=8 , required=False)
    is_superuser = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop('type', None)
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if not phone:
            raise ValidationError([
                ValidationError('شماره موبایل الزامی است!', code='phone'),
            ])

        if self.type == 'CREATE':
            if not password:
                raise ValidationError([
                    ValidationError('رمز عبور الزامی است!', code='password'),
                ])

            if not password2:
                raise ValidationError([
                    ValidationError('تکرار رمز عبور الزامی است!', code='password2'),
                ])

            if password != password2:
                raise ValidationError([
                    ValidationError('رمز عبور با تکرار آن مغایرت دارد!', code='password'),
                ])

            query = Q(phone=phone)

            if User.objects.filter(query).exists():
                raise ValidationError([
                    ValidationError('کاربری با این ایمیل/موبایل قبلا ثبت شده است!', code='duplicate'),
                ])

        else:
            check_user_exist(self.user, phone)

        return cleaned_data