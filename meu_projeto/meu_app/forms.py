from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'data_compra': forms.DateInput(attrs={'type': 'date'})
        }