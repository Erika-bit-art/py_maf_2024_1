from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('adicionar_registro/', views.adicionar_registro, name='adicionar_registro'),
    path('admin/biblioteca/', include([
        path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
        path('logout/', views.logout, name='logout'),
    ])),
]