from django.core.management.base import BaseCommand
from wayzata76_web.models import Gallery
import json
from django.conf import settings
from django.templatetags.static import static


class Command(BaseCommand):
    help = "Instantiates Gallery Objects from Target JSON file"

    def handle(self, *args, **kwargs):
        json_file = "static/json/gallery.json"  # relative path is from folder calling the command -->'manage.py' aka wayzata76_app aka PROJECT_ROOT
        with open(json_file) as gallery_json:
            json_data = json.load(gallery_json)
            gallery_count = 0
            section_lookup = {
                "REUNIONS": ("REUNIONS", "Reunions"),
                "STUDENT_LIFE": ("STUDENT_LIFE", "Student Life"),
                "STOMPING_GROUNDS": ("STOMPING_GROUNDS", "The Stomping Grounds"),
            }
            for record in json_data:
                if record["parent_working_name"]:
                    parent_gallery = Gallery.objects.filter(
                        working_name=record["parent_working_name"]
                    ).first()
                else:
                    parent_gallery = None
                new_gallery = Gallery(
                    working_name=record["working_name"],
                    display_name=record["display_name"],
                    section=section_lookup[record["section"]]
                    if record["section"]
                    else None,
                    abstract_gallery=record["abstract_gallery"],
                    subgallery=record["subgallery"],
                    parent_gallery=parent_gallery,
                )
                new_gallery.save()
                gallery_count += 1