from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from django.core.management import call_command

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registros/', include('registros.urls')),
    path('', lambda request: redirect('registros/', permanent=True)),
]

call_command('create_superuser_if_not_exists')


# Adiciona as configurações para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
