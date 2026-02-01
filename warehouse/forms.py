from django import forms
from .models import Input


class InputForm(forms.ModelForm):
    class Meta:
        model = Input
        fields = ['product', 'quantity', 'price', 'summa']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_quantity'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_price'}),
            'summa': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'id_summa'}),
        }
