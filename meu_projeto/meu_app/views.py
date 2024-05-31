from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Compra, Nota
from .forms import CompraForm, BuscaForm, NotaForm
import json
from decimal import Decimal

def criar_nota(request, compra_id=None):
    if compra_id:
        compra = get_object_or_404(Compra, pk=compra_id)
    else:
        compra = None


    form = NotaForm()

    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.compra = compra
            nota.save()
            return redirect('listar_notas')
    
    
    return render(request, 'criar_nota.html', {'form': form, 'compra': compra})

def criar_nota_compra(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.compra = compra
            nota.save()
            return redirect('listar_notas')  
    else:
        form = NotaForm()
    return render(request, 'criar_nota.html', {'form': form, 'compra': compra})

def listar_notas(request):
    notas = Nota.objects.all()
    return render(request, 'listar_notas.html', {'notas': notas})

def ver_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    return render(request, 'ver_nota.html', {'nota': nota})


def editar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            return redirect('listar_notas') 
    else:
        form = NotaForm(instance=nota)
    return render(request, 'criar_nota.html', {'form': form, 'compra': nota.compra})

def deletar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        nota.delete()
        return redirect('listar_notas') 
    return render(request, 'confirmar_delete_nota.html', {'nota': nota})

def deletar_notas(request):
    if request.method == 'POST':
        notas_ids = request.POST.getlist('notas_a_deletar[]')
        notas = Nota.objects.filter(id__in=notas_ids)
        notas.delete()
    return redirect('listar_notas')

def lista_compras(request):
    compras = Compra.objects.all()
    busca_form = BuscaForm(request.GET)

    if busca_form.is_valid():
        busca = busca_form.cleaned_data['busca']
        data_inicio = busca_form.cleaned_data['data_inicio']
        data_fim = busca_form.cleaned_data['data_fim']
        valor_minimo = busca_form.cleaned_data['valor_minimo']
        valor_maximo = busca_form.cleaned_data['valor_maximo']

        if busca:
            compras = compras.filter(texto_busca__icontains=busca)
        if data_inicio:
            compras = compras.filter(data_compra__gte=data_inicio)
        if data_fim:
            compras = compras.filter(data_compra__lte=data_fim)
        if valor_minimo:
            compras = compras.filter(valor__gte=valor_minimo)
        if valor_maximo:
            compras = compras.filter(valor__lte=valor_maximo)


    filtros = {
        'nome': request.COOKIES.get('nome', 'off'),
        'email': request.COOKIES.get('email', 'off'),
        'numero': request.COOKIES.get('numero', 'off'),
        'data_compra': request.COOKIES.get('data_compra', 'off'),
        'pacote': request.COOKIES.get('pacote', 'off'),
        'valor': request.COOKIES.get('valor', 'off'),
        'taxa_catarse': request.COOKIES.get('taxa_catarse', 'off'),
        'faturamento': request.COOKIES.get('faturamento', 'off'),
        'acoes': request.COOKIES.get('acoes', 'off'),
    }


    if filtros['nome'] == 'on':
        compras = compras.exclude(nome__isnull=True).exclude(nome__exact='')
    if filtros['email'] == 'on':
        compras = compras.exclude(email__isnull=True).exclude(email__exact='')
    if filtros['numero'] == 'on':
        compras = compras.exclude(numero__isnull=True)
    if filtros['data_compra'] == 'on':
        compras = compras.exclude(data_compra__isnull=True)
    if filtros['pacote'] == 'on':
        compras = compras.exclude(pacote__isnull=True).exclude(pacote__exact='')
    if filtros['valor'] == 'on':
        compras = compras.exclude(valor__isnull=True)
    if filtros['taxa_catarse'] == 'on':
        compras = [c for c in compras if c.taxa_catarse > Decimal('0.00')] 
    if filtros['faturamento'] == 'on':
        compras = [c for c in compras if c.faturamento > Decimal('0.00')] 

        

    return render(request, 'lista_compras.html', {
        'compras': compras,
        'filtros': filtros,
        'busca_form': busca_form,
    })



def nova_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)  
            compra.data_compra = form.cleaned_data['data_compra'].strftime('%Y-%m-%d')  
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


    filtros = {
        'nome': request.COOKIES.get('nome', 'off'),
        'email': request.COOKIES.get('email', 'off'),
        'numero': request.COOKIES.get('numero', 'off'),
        'data_compra': request.COOKIES.get('data_compra', 'off'),
        'pacote': request.COOKIES.get('pacote', 'off'),
        'valor': request.COOKIES.get('valor', 'off'),
        'taxa_catarse': request.COOKIES.get('taxa_catarse', 'off'),
        'faturamento': request.COOKIES.get('faturamento', 'off'),
    }


    data = []
    for compra in compras:
        compra_data = {}
        if filtros['nome'] == 'on':
            compra_data['nome'] = compra.nome
        if filtros['email'] == 'on':
            compra_data['email'] = compra.email
        if filtros['numero'] == 'on':
            compra_data['numero'] = compra.numero
        if filtros['data_compra'] == 'on':
            compra_data['data_compra'] = compra.data_compra.strftime('%Y-%m-%d')
        if filtros['pacote'] == 'on':
            compra_data['pacote'] = compra.pacote
        if filtros['valor'] == 'on':
            compra_data['valor'] = str(compra.valor)
        if filtros['taxa_catarse'] == 'on':
            compra_data['taxa_catarse'] = str(compra.taxa_catarse)
        if filtros['faturamento'] == 'on':
            compra_data['faturamento'] = str(compra.faturamento)
        data.append(compra_data)


    formato = request.GET.get('formato', 'estruturado')
    if formato == 'simples':

        conteudo = "\n".join([";".join(item.values()) for item in data])
        content_type = 'text/plain'
        filename = 'compras.txt'
    else:
   
        conteudo = json.dumps(data)
        content_type = 'application/json'
        filename = 'compras.json'

    response = HttpResponse(conteudo, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response