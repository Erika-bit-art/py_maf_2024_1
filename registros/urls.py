from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('editar/<int:registro_id>/', views.editar_registro, name='editar_registro'),
    path('excluir/<int:registro_id>/', views.excluir_registro, name='excluir_registro'),
    path('adicionar_registro/', views.adicionar_registro, name='adicionar_registro'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('resend_activation_email/<int:usuario_id>/', views.resend_activation_email, name='resend_activation_email'),
    path('admin/biblioteca/', include([
        path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
        path('usuarios/desativar/<int:usuario_id>/', views.desativar_usuario, name='desativar_usuario'),
        path('usuarios/reativar/<int:usuario_id>/', views.reativar_usuario, name='reativar_usuario'),
        path('usuarios/excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
    ])),

    path('', views.dashboard, name='dashboard'),
    path('change_password/', views.change_password, name='change_password'),

]