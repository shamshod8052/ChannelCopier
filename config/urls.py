from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.views.static import serve

from Admin.views import healthz

urlpatterns = [
    path('healthz', healthz),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
