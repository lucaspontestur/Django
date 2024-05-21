from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Compra
from .forms import CompraForm, BuscaForm
import json
from decimal import Decimal

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

    # Obter os filtros dos cookies
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

    # Aplicar os filtros à consulta (adaptando para propriedades calculadas)
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
        compras = [c for c in compras if c.taxa_catarse > Decimal('0.00')] # Filtra propriedades
    if filtros['faturamento'] == 'on':
        compras = [c for c in compras if c.faturamento > Decimal('0.00')] # Filtra propriedades

        

    # Renderizar o template com as compras filtradas e os filtros atuais
    return render(request, 'lista_compras.html', {
        'compras': compras,
        'filtros': filtros,
        'busca_form': busca_form,
    })



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

    # Obter os filtros dos cookies
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

    # Filtrar os dados com base nos filtros dos cookies
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

    # Escolher o formato de download
    formato = request.GET.get('formato', 'estruturado')
    if formato == 'simples':
        # Criar uma string com as informações separadas por quebra de linha
        conteudo = "\n".join([";".join(item.values()) for item in data])
        content_type = 'text/plain'
        filename = 'compras.txt'
    else:
        # JSON estruturado
        conteudo = json.dumps(data)
        content_type = 'application/json'
        filename = 'compras.json'

    response = HttpResponse(conteudo, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response