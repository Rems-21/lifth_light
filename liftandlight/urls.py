"""
URL configuration for liftandlight project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from projets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projets.urls')),
    path('blog/', include('blog.urls')),
    # Servir les fichiers HTML statiques avec remplacement des chemins
    re_path(r'^ascenceur/(?P<path>.*\.html)$', views.serve_static_html),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

