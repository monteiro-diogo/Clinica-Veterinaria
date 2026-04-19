from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Alterado de 'workshop.urls' para 'core.urls' conforme a sua nova estrutura
    path('', include('core.urls')),
]

# Mantém a configuração para servir ficheiros de media (como fotos de animais) em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)