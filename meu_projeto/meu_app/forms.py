from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    data_compra = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Widget para data
        input_formats=['%Y-%m-%d'],  # Formato de entrada
    )

    class Meta:
        model = Compra
        fields = '__all__'

    class Media:
        js = ('js/jquery-3.6.0.min.js', 'js/jquery.mask.min.js', 'js/mascara.js')