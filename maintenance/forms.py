from django import forms
from .models import MaintenanceBill
from residents.models import Resident

class MaintenanceBillForm(forms.ModelForm):
    class Meta:
        model = MaintenanceBill
        fields = ['resident', 'amount', 'due_date', 'status']
        widgets = {
            'resident': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
