from django.urls import path
from meu_app import views

urlpatterns = [
    path('', views.lista_compras, name='lista_compras'),
    path('nova/', views.nova_compra, name='nova_compra'),
    path('editar/<int:pk>/', views.editar_compra, name='editar_compra'),
    path('deletar/<int:pk>/', views.deletar_compra, name='deletar_compra'),
    path('download/', views.download_compras, name='download_compras'),
    
    path('nota/criar/<int:compra_id>/', views.criar_nota, name='criar_nota_compra'),
    path('nota/criar/', views.criar_nota, name='criar_nota'),
    path('notas/', views.listar_notas, name='listar_notas'),
    path('nota/<int:pk>/ver/', views.ver_nota, name='ver_nota'),
    path('nota/<int:pk>/editar/', views.editar_nota, name='editar_nota'),
    path('nota/<int:pk>/deletar/', views.deletar_nota, name='deletar_nota'),
    path('notas/deletar/', views.deletar_notas, name='deletar_notas'),
]