from django import forms
from .models import Input


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['product', 'quantity', 'price', 'summa']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control comma-number', 'id': 'id_quantity', 'inputmode': 'decimal'}),
            'price': forms.TextInput(attrs={'class': 'form-control comma-number', 'id': 'id_price', 'inputmode': 'decimal'}),
            'summa': forms.TextInput(attrs={'class': 'form-control comma-number', 'readonly': 'readonly', 'id': 'id_summa'}),
        }
