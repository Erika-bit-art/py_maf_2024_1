from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('personalizar/', views.personalizar, name='personalizar'),
    path('dashboard/', views.dashbord, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]
