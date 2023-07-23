from django.contrib import admin
from django.urls import re_path, include
from where_to_go import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path("admin/", admin.site.urls),
    re_path("", views.show_map)
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
