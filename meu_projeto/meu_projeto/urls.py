from django.urls import path
from meu_app import views

urlpatterns = [
    path('', views.lista_compras, name='lista_compras'),
    path('nova/', views.nova_compra, name='nova_compra'),
    path('editar/<int:pk>/', views.editar_compra, name='editar_compra'),
    path('deletar/<int:pk>/', views.deletar_compra, name='deletar_compra'),
]