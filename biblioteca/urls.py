from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.login, name='login'),
    path('adicionar/', views.adicionar_livro, name='adicionar_livro'),
    path('admin/biblioteca/', include([
        path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
        path('desativar_usuario/<int:usuario_id>/', views.desativar_usuario, name='desativar_usuario'),
        path('reativar_usuario/<int:usuario_id>/', views.reativar_usuario, name='reativar_usuario'),
        path('excluir_usuario/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    ])),
    path('logout/', views.logout, name='logout'),
]

