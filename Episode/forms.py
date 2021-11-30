from django import forms
from .models import *

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = '__all__'