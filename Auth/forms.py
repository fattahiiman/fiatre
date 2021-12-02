from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_integer, RegexValidator
from django.utils.regex_helper import _lazy_re_compile
from .helpers import *

User = get_user_model()


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=255, min_length=11, required=True)
    password = forms.CharField(max_length=100, required=True)
    remember_me = forms.BooleanField(required=False , initial=False)


class RegisterForm(forms.Form):
    phone = forms.CharField(max_length=255, min_length=11, required=True, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="شماره موبایل باید عددی باشد",
    )])
    password = forms.CharField(max_length=100, required=True)
    password2 = forms.CharField(max_length=100, required=True)
    remember_me = forms.BooleanField(required=False , initial=False)

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError([
                ValidationError('رمز عبور با تکرار آن مغایرت دارد!', code='password'),
            ])

        check_user_exist(phone)

        return cleaned_data


class ResetPasswordForm(forms.Form):
    phone = forms.CharField(max_length=255, min_length=11, required=True, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="شماره موبایل باید عددی باشد",
    )])


class ResetPasswordConfirmForm(forms.Form):
    code = forms.CharField(max_length=5, min_length=5, required=True, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="کد تایید باید عددی باشد",
    )])


class ResetPasswordEnterForm(forms.Form):
    password = forms.CharField(max_length=100, min_length=8, required=True)
    password2 = forms.CharField(max_length=100, min_length=8, required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError([
                ValidationError('رمز عبور با تکرار آن مغایرت دارد!', code='password'),
            ])

        return cleaned_data


class LoginCodeForm(forms.Form):
    phone = forms.CharField(max_length=255, min_length=11, required=True, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="شماره موبایل باید عددی باشد",
    )])


class LoginCodeConfirmForm(forms.Form):
    code = forms.CharField(max_length=5, min_length=5, required=True, validators=[RegexValidator(
        regex=r'^-?\d+\Z',
        message="کد تایید باید عددی باشد",
    )])