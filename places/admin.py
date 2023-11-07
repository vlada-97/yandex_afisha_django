from django.contrib import admin

from .models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from adminsortable2.admin import SortableAdminBase, SortableTabularInline


def get_html_preview(image):
    return format_html(
        '<img src="{url}" height={height}/>',
        url=image.image.url,
        height=200,
    )


class ImageInline(SortableTabularInline):
    model = Image

    readonly_fields = [
        "get_preview",
    ]

    @staticmethod
    def get_preview(obj):
        return get_html_preview(obj)

    get_preview.short_description = "Фото превью"


@admin.register(Place)
class AdminPlace(SortableAdminBase, admin.ModelAdmin):
    search_fields = [
        "title",
    ]
    list_display = [
        "title",
        "get_preview",
    ]
    inlines = [
        ImageInline,
    ]

    def get_preview(self, obj):
        return get_html_preview(obj.images.first())

    get_preview.short_description = "Фото превью"

    def get_preview_readonly(self, obj):
        return self.get_preview(obj)

    get_preview_readonly.short_description = "Фото превью"
    get_preview_readonly.readonly = True

    readonly_fields = ["get_preview_readonly"]

    get_preview.admin_order_field = "images__image"


@admin.register(Image)
class AdminImage(SortableAdminMixin, admin.ModelAdmin):
    fields = (
        "place",
        "image",
        "get_preview",
    )
    list_display = [
        "position",
        "place",
        "get_preview",
    ]
    list_filter = ["place"]
    readonly_fields = [
        "get_preview",
    ]

    @staticmethod
    def get_preview(obj):
        return get_html_preview(obj)

    get_preview.short_description = "Фото превью"
