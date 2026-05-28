from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Esta linha é a que "liga" o dashboard que queremos usar!
    path('admin/', admin.site.urls),
    
    # Esta linha tu já deves ter aí (que liga às páginas normais do site)
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)