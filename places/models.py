from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        "Название",
        max_length=150,
    )
    short_description = models.TextField(
        "Краткое описание",
        blank=True,
    )
    long_description = HTMLField(
        "Описание",
        blank=True,
    )
    lng = models.FloatField(
        "Долгота",
    )
    lat = models.FloatField(
        "Широта",
    )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(
        "Картинка",
    )
    position = models.IntegerField(
        "Позиция",
        default=0,
        db_index=True,
    )
    place = models.ForeignKey(
        "Place",
        on_delete=models.CASCADE,
        verbose_name="Место",
        related_name="images",
    )

    class Meta:
        ordering = ("position",)
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.place.title
