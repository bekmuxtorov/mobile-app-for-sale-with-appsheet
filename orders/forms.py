from django import forms
from .models import Output


class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        fields = ['product', 'customer', 'quantity', 'price', 'is_payment']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_payment': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-top: 10px;'}),
        }
