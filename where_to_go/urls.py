from django.contrib import admin
from django.urls import re_path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path("admin/", admin.site.urls),
    re_path("", include("places.urls")),
    re_path("tinymce/", include("tinymce.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
