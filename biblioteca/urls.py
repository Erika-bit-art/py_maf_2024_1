from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('login/', views.login, name='login'),
    path('adicionar/', views.adicionar_livro, name='adicionar_livro'),
    path('logout/', views.logout, name='logout'),


]


