from django.core.management.base import BaseCommand
from wayzata76_web.models import SubGallery, Gallery
import json
from django.conf import settings


class Command(BaseCommand):
    help="Instantiate SubGallery objects from JSON file @ staticfile/json/subgallery.json"

    def handle(self, *args, **kwargs):
        json_file = 'staticfiles/json/subgallery.json'
        with open(json_file) as subgallery_json:
            json_data = json.load(subgallery_json)
            subgallery_count = 0
            for record in json_data:
                parent_gallery = Gallery.objects.filter(working_name=record['parent_working_name']).first()
                if parent_gallery:
                    new_subgallery = SubGallery(
                        parent=parent_gallery,
                        working_name=record['working_name'],
                        display_name=record['display_name']
                    )
                    new_subgallery.save()
                    subgallery_count += 1
                    print(f'New SubGallery Added: {new_subgallery.display_name} to {new_subgallery.parent.display_name}')
                else:
                    print(f"No parent gallery found with working_name = {record['parent_working_name']}")
            print(f'Total SubGalleries Added = {subgallery_count}')
            