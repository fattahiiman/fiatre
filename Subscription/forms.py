from django import forms
from .models import *

class SubscriptionTypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'



class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'