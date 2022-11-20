from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework import permissions


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/', include("api.v1.urls")),
   path('__debug__/', include('debug_toolbar.urls')),
   
   re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
   re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += [
    re_path(r'^docs/(?P<path>.*)', serve, {'document_root': settings.DOCS_ROOT})
] + static(settings.DOCS_URL, document_root=settings.DOCS_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
