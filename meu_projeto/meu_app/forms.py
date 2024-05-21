from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    data_compra = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Compra
        fields = ['nome', 'email', 'numero', 'data_compra', 'pacote', 'valor'] 

    class Media:
        js = ('js/jquery-3.6.0.min.js', 'js/jquery.mask.min.js', 'js/mascara.js')

class BuscaForm(forms.Form):
    busca = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Digite sua busca...'}),
    )
    data_inicio = forms.DateField(
        label='Data de Início',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )
    data_fim = forms.DateField(
        label='Data de Fim',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )
    valor_minimo = forms.DecimalField(
        label='Valor Mínimo',
        required=False,
    )
    valor_maximo = forms.DecimalField(
        label='Valor Máximo',
        required=False,
    )