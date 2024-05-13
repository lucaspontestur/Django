from django.shortcuts import render, redirect, get_object_or_404
from .models import Compra
from .forms import CompraForm

def lista_compras(request):
    compras = Compra.objects.all()
    return render(request, 'lista_compras.html', {'compras': compras})

def nova_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()
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