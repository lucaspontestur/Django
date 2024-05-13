from django.shortcuts import render, redirect
from .models import Texto

def enviar_texto(request):
    if request.method == 'POST':
        texto = request.POST.get('texto')
        Texto.objects.create(conteudo=texto)
        return redirect('lista_textos')
    return render(request, 'enviar_texto.html')

def index(request):
    return render(request, 'index.html')

def lista_textos(request):
    textos = Texto.objects.all()
    return render(request, 'lista_textos.html', {'textos': textos})