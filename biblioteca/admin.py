from django.contrib import admin
from .models import Usuario, Livro

# Personalizando a exibição do modelo Usuario no admin
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'idade', 'is_active', 'is_admin', 'created_at')
    search_fields = ('email', 'nome')
    list_filter = ('is_active', 'is_admin')
    ordering = ('-created_at',)

# Registrando o modelo Usuario
admin.site.register(Usuario, UsuarioAdmin)

# Registrando o modelo Livro
admin.site.register(Livro)