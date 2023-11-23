from adminsortable2.admin import (SortableAdminBase, SortableAdminMixin,
                                  SortableTabularInline)
from django.contrib import admin
from django.utils.html import format_html

from .models import Image, Place


def get_html_preview(image):
    return format_html(
        "<img src='{url}' style='max-height: 200px; max-width: 200px'>",
        url=image.image.url,
    )


class ImageInline(SortableTabularInline):
    model = Image

    readonly_fields = [
        "get_html_preview_readonly",
    ]

    @staticmethod
    def get_html_preview_readonly(obj):
        return get_html_preview(obj)

    get_html_preview_readonly.short_description = "Фото превью"


@admin.register(Place)
class AdminPlace(SortableAdminBase, admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "get_image_preview"]
    inlines = [ImageInline]

    def get_image_preview(self, obj):
        first_image = obj.images.first()
        return self.get_html_preview_readonly(first_image) if first_image else ""

    get_image_preview.short_description = "Фото превью"

    def get_html_preview_readonly(self, obj):
        return get_html_preview(obj)

    get_html_preview_readonly.short_description = "Фото превью"
    get_html_preview_readonly.readonly = True

    readonly_fields = ["get_html_preview_readonly"]

    get_image_preview.admin_order_field = "images__image"


@admin.register(Image)
class AdminImage(SortableAdminMixin, admin.ModelAdmin):
    raw_id_fields = ("place",)
    list_display = [
        "position",
        "place",
        "get_html_preview",
    ]
    list_filter = ["place"]
    readonly_fields = [
        "get_html_preview",
    ]

    @staticmethod
    def get_html_preview(obj):
        return get_html_preview(obj)

    get_html_preview.short_description = "Фото превью"
