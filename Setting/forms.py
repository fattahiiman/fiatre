from django import forms
from .models import *

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'