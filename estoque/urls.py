from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registrar_usuario, name='registrar_usuario'),

    # URL para a página de login
    path('login/', views.login, name='login'),  # Usando a view de login padrão do Django

    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('admin/biblioteca/', include([
        path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
        path('logout/', views.logout, name='logout'),  # Certifique-se de que a view de logout está implementada
    ])),
]