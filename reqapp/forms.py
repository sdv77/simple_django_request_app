from django import forms
from .models import Request, Device

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['device', 'description']