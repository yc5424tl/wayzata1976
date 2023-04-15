from django.core.management.base import BaseCommand
from wayzata76_web.models import Person, Address
import json
from django.conf import settings

from django.templatetags.static import static


class Command(BaseCommand):
    help = "Instantiates Person objects from target JSON file"

    def handle(self, *args, **kwargs):
        json_file = "../../static/json/class_list.json"
        with open(json_file) as class_list_json:
            json_data = json.load(class_list_json)
            classmate_count = 0
            address_count = 0
            for record in json_data:
                last_name = record["last_name"]
                first_name = record["first_name"]
                middle_initial = record["middle_initial"]
                city = record["city"]
                state = record["state"]
                zip_code = record["zip"]

                new_address = None

                if record['city'].strip() not in ['UNKNOWN', 'passed', '']:

                    new_address = Address(
                        city=city, state_province=state, zip_code=zip_code
                    )
                    new_address.save()
                    address_count += 1
                if record["city"] == "passed":
                    new_address = Address(city="passed")
                    new_address.save()
                new_person = Person(
                    last_name=last_name,
                    first_name=first_name,
                    middle_initial=middle_initial,
                    address=new_address,
                )
                new_person.save()
                classmate_count += 1

            print(
                f"Added {classmate_count} classmate(s) and {address_count} address(es)"
            )
