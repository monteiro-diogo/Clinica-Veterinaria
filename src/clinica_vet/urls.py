from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Esta linha é a que "liga" o dashboard que queremos usar!
    path('admin/', admin.site.urls),
    
    # Esta linha tu já deves ter aí (que liga às páginas normais do site)
    path('', include('core.urls')),
]