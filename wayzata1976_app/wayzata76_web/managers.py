from .models import Address, Person
import json



def build_objects_from_classlist(json_file):
    json_data = json.load(open(json_file))
    for record in json_data:
        new_person = extract_person(record)
        print(f'new person {new_person.last_name}, {new_person.first_name} from json')
        new_address = extract_address(record)
        if new_address:
            new_person.address = new_address
            print('new address {new_address} added for person')
        new_person.save()


def extract_address(record):
    try:
        city = record["city"]
        state = record["state"]
        zip = record["zip"]
        new_address = Address(city=city, state_province=state, zip=zip)
        new_address.save()
        return new_address
    except KeyError as kE:
        print('extract address key error')
        return None


def extract_person(record):
    try:
        last_name = record["last_name"]
        first_name = record["first_name"]
        middle_initial = record["middle_initial"]
        new_person = Person(last_name=last_name, first_name=first_name, middle_initial=middle_initial)
        return new_person
    except KeyError as kE:
        print('extract person key error')
        return None


# >>> from wayzata76_web import managers
# >>> from django.conf import settings
# >>> managers.build_objects_from_classlist(f'{settings.BASE_DIR}{settings.STATIC_URL}json/class_list.json')