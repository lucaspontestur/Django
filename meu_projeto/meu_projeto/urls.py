from django.urls import path
from meu_app import views
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('enviar_texto')),  # Redireciona para /enviar/
    path('enviar/', views.enviar_texto, name='enviar_texto'),
    path('lista/', views.lista_textos, name='lista_textos'),
]