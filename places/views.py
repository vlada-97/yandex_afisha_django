from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Image, Place


def index(request):
    serialized_places = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [place.lng, place.lat]},
            "properties": {
                "title": place.title,
                "placeId": place.pk,
                "detailsUrl": reverse("detail", args=(place.pk,)),
            },
        }
        for place in Place.objects.all()
    ]

    collection = {"type": "FeatureCollection", "features": serialized_places}
    return render(request, "places/index.html", context={"places": collection})


def get_place_detail(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related(
            Prefetch(
                "images",
                queryset=Image.objects.order_by("position"),
                to_attr="ordered_images",
            )
        ),
        pk=place_id,
    )

    content = {
        "title": place.title,
        "imgs": [img.image.url for img in place.ordered_images],
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {"lat": place.lat, "lng": place.lng},
    }

    return JsonResponse(content, json_dumps_params={"ensure_ascii": False, "indent": 2})
