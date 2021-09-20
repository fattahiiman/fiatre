from django import forms
from .models import *

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'


class SubscriptionBuyCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code']