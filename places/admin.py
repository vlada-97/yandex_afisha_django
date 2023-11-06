from django.contrib import admin

from .models import Place, Image

from django.contrib import admin

from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Place)
class AdminPlace(admin.ModelAdmin):
    search_fields = [
        "title",
    ]
    list_display = [
        "title",
    ]
    inlines = [
        ImageInline,
    ]


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    fields = (
        "place",
        "image",
    )
    list_display = [
        "position",
        "place",
    ]
    list_filter = [
        "place",
    ]
