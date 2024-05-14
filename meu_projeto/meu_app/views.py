from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Compra
from .forms import CompraForm
import json

def lista_compras(request):
    compras = Compra.objects.all()
    return render(request, 'lista_compras.html', {'compras': compras})

def nova_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)  # Não salve ainda
            compra.data_compra = form.cleaned_data['data_compra'].strftime('%Y-%m-%d')  # Formata a data
            compra.save()
            return redirect('lista_compras')
    else:
        form = CompraForm()
    return render(request, 'nova_compra.html', {'form': form})

def editar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            return redirect('lista_compras')
    else:
        form = CompraForm(instance=compra)
    return render(request, 'editar_compra.html', {'form': form})

def deletar_compra(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        compra.delete()
        return redirect('lista_compras')
    return render(request, 'confirmar_delete.html', {'compra': compra})

def download_compras(request):
    compras = Compra.objects.all()
    
    # Filtrar os dados com base nas colunas selecionadas
    data = []
    for compra in compras:
        compra_data = {}
        if request.GET.get('nome'):
            compra_data['nome'] = compra.nome
        if request.GET.get('email'):
            compra_data['email'] = compra.email
        if request.GET.get('numero'):
            compra_data['numero'] = compra.numero
        if request.GET.get('data_compra'):
            compra_data['data_compra'] = compra.data_compra.strftime('%Y-%m-%d')
        if request.GET.get('pacote'):
            compra_data['pacote'] = compra.pacote
        if request.GET.get('valor'):
            compra_data['valor'] = str(compra.valor)
        if request.GET.get('taxa_catarse'):
            compra_data['taxa_catarse'] = str(compra.taxa_catarse)
        if request.GET.get('faturamento'):
            compra_data['faturamento'] = str(compra.faturamento)
        data.append(compra_data)

    # Escolher o formato de download (JSON neste exemplo)
    response = HttpResponse(json.dumps(data), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="compras.json"'
    return response