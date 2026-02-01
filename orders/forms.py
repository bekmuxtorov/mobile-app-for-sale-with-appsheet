from django import forms
from .models import Output


class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        fields = ['product', 'customer', 'quantity', 'price', 'is_payment']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control comma-number', 'id': 'id_quantity', 'inputmode': 'decimal'}),
            'price': forms.TextInput(attrs={'class': 'form-control comma-number', 'id': 'id_price', 'inputmode': 'decimal'}),
            'is_payment': forms.CheckboxInput(attrs={'class': 'switch-input', 'role': 'switch'}),
        }
        labels = {
            'is_payment': "To'lov qilinganlik holati"
        }
