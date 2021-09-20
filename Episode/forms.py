from django import forms
from .models import *

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'


    def clean(self):
        print('---------------------')
        print(self.cleaned_data.get('title'))