from django import forms
from .models import Visitor

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['visitor_name', 'visit_date', 'purpose']
        widgets = {
            'visitor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter visitor name'}),
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Purpose of visit (e.g. Delivery, Family)'}),
        }
