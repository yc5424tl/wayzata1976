from django.core.management.base import BaseCommand
from wayzata76_web.models import Person, Address
import json
from django.conf import settings
# from django.templatetags.static import static
from django.templatetags.static import static
class Command(BaseCommand):
    help = 'Instantiates Person objects from target JSON file'

    def handle(self, *args, **kwargs):
        json_file = "/home/j/dev/repo/wayzata1976/wayzata1976_app"+static('json/class_list.json')
        with open(json_file) as class_list_json:
            json_data = json.load(class_list_json)
            classmate_count = 0
            address_count = 0
            for record in json_data:
                last_name = record['last_name']
                first_name = record['first_name']
                middle_initial = record['middle_initial']
                city = record['city']
                state = record['state']
                zip_code = record['zip']

                new_address = None
                if record['city'] != 'UNKNOWN' and record['city'].strip() != '' and record['city'] != 'passed':
                    new_address = Address(city=city, state_province=state, zip_code=zip_code)
                    new_address.save()
                    address_count += 1
                new_person = Person(last_name=last_name, first_name=first_name, middle_initial=middle_initial, address=new_address)
                new_person.save()
                classmate_count += 1

            print(f'Added {classmate_count} classmate(s) and {address_count} address(es)')

    # def add_arguments(self, parser):
        # parser.add_argument('json_file', type=str, help='Path to target JSON file')