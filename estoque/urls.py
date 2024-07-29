from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views

urlpatterns = [

    path('editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('excluir/<int:produto_id>/', views.excluir_produto, name='excluir_produto'),
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.login, name='login'),
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('admin/biblioteca/', include([
        path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
        path('logout/', views.logout, name='logout'),
    ])),
]

