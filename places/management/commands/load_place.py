import json
from hashlib import md5
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from places.models import Image, Place


def get_json_url(raw_url):
    url = urlparse(raw_url)
    if all((url.scheme, url.netloc)):
        return raw_url
    raise CommandError("Invalid URL")


def create_place(raw_place_attributes):
    try:
        place, created = Place.objects.get_or_create(
            lng=raw_place_attributes["coordinates"]["lng"],
            lat=raw_place_attributes["coordinates"]["lat"],
            defaults={
                "title": raw_place_attributes["title"],
                "short_description": raw_place_attributes.get("description_short", ""),
                "long_description": raw_place_attributes.get("description_long", ""),
            },
        )
        return place, created
    except KeyError:
        raise CommandError("No required fields found! Use JSON format from README.md!")
    except MultipleObjectsReturned:
        print("Multiple objects returned for the given coordinates.")
    except Place.DoesNotExist:
        print("Place does not exist for the given coordinates.")


def add_images(obj, place_attributes, place):
    try:
        place_attributes["imgs"]
    except KeyError:
        obj.stdout.write(obj.style.WARNING("No images found!"))
        return
    for position, image_url in enumerate(place_attributes["imgs"]):
        image_content = requests.get(image_url).content
        image_name = md5(image_content).hexdigest() + Path(image_url).suffix
        content_file = ContentFile(
            image_content,
            name=image_name,
        )
        Image.objects.create(
            place=place,
            image=content_file,
            position=position,
        )
        obj.stdout.write(obj.style.SUCCESS(f"Image {image_name} saved!"))


class Command(BaseCommand):
    help = "Add new point to map"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=Path,
            help="Path to JSON file",
        )
        parser.add_argument(
            "--url",
            type=get_json_url,
            help="URL to JSON file",
        )
        parser.add_argument(
            "--skip_imgs",
            action="store_true",
            help="Skip uploading images",
        )

    def handle(self, *args, **options):
        if options["file"] and options["url"]:
            raise CommandError(
                'Both arguments("url" and "file") are specified. Choose one!'
            )
        elif options["file"]:
            json_path = Path.joinpath(settings.BASE_DIR, options["file"])
            if not Path.exists(json_path):
                raise CommandError("File not found!")
            with open(json_path, "r", encoding="utf-8") as file:
                try:
                    place_attributes = json.load(file)
                except json.JSONDecodeError:
                    raise CommandError("Wrong file type, JSON needed!")
        elif options["url"]:
            response = requests.get(options["url"])
            response.raise_for_status()
            place_attributes = response.json()
        else:
            raise CommandError("No action requested. Add argument!")

        raw_place_attributes = place_attributes

        place, created = create_place(raw_place_attributes)
        if not created:
            self.stdout.write(
                self.style.WARNING(f'{raw_place_attributes["title"]} already exists!')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'Place {raw_place_attributes["title"]} created!')
        )
        if not options["skip_imgs"]:
            add_images(self, raw_place_attributes, place)
