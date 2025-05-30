from django import forms
from .models import Request, Device, Category
from django.contrib.auth.models import User


class RequestForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Категория')

    class Meta:
        model = Request
        fields = ['category', 'device', 'description']

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['device'].queryset = Device.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['device'].queryset = self.instance.category.devices.order_by('name')
        else:
            self.fields['device'].queryset = Device.objects.none()

class ChangeStatusForm(forms.Form):
    STATUS_CHOICES = Request.STATUS_CHOICES

    status = forms.ChoiceField(choices=STATUS_CHOICES)
    technician = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Technician'), required=True)  # Только техники могут изменять статус
