from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('editar/<int:registro_id>/', views.editar_registro, name='editar_registro'),
    path('excluir/<int:registro_id>/', views.excluir_registro, name='excluir_registro'),
    path('', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro, name='cadastro'),

    path('login/', views.login, name='login'),

    path('adicionar_registro/', views.adicionar_registro, name='adicionar_registro'),
    path('admin/biblioteca/', include([
        path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
        path('admin/usuarios/desativar/<int:usuario_id>/', views.desativar_usuario, name='desativar_usuario'),
        path('admin/usuarios/reativar/<int:usuario_id>/', views.reativar_usuario, name='reativar_usuario'),
        path('admin/usuarios/excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
        path('logout/', views.logout, name='logout'),
    ])),
]