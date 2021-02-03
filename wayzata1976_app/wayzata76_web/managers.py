from .models import Address, Person
import json
# from django.db.utils import IntegrityError
# from django.db import IntegrityError
# from sqlite3 import IntegrityError
import sqlite3
import django.db
from django.db.backends.sqlite3.base import IntegrityError


def build_objects_from_classlist(json_file):
    json_data = json.load(open(json_file))
    for record in json_data:
        try:
            new_person = extract_person(record)
            if new_person:
                print(f'new person {new_person.last_name}, {new_person.first_name} from json')
                new_address = extract_address(record)
                if new_address:
                    new_person.address = new_address
                    print('new address {new_address} added for person')
                new_person.save()
        except IntegrityError as iE:
            print(f'IntegrityError from build_objects_from_classlist: {iE.message}')
            continue
        # except django.db.IntegrityError as iE:
        #     print(f'djangodb interr : {iE.message}')
        #     continue
        # except django.db.utils.IntegrityError as iE:
        #     print(f'django.db.utils.integrityerror {iE.message}')
        # except:
        #     print('build object catch all except')
        #     continue


def extract_address(record):
    try:
        city = record["city"]
        state = record["state"]
        zip_code = record["zip"]
        new_address = Address(city=city, state_province=state, zip_code=zip_code)
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
    except IntegrityError as iE:
        print(f'sqlite3 IntegrityError instantiating new person {last_name}, {first_name} {middle_initial}')
        return None
    # except django.db.IntegrityError as iE:
    #     print(f'django.db integrity error: {iE.message}')
    #     return None
    # except django.db.utils.IntegrityError as iE:
    #     print(f'django.db.utils.IntegrityError {iE.message}')
    #     return None
    # except:
    #     print('catch all except')
    #     return None

# export DJANGO_SETTINGS_MODULE="wayzata76_django.settings"
# import django
# django.setup()
# >>> from wayzata76_web import managers
# >>> from django.conf import settings
# >>> managers.build_objects_from_classlist(f'{settings.BASE_DIR}{settings.STATIC_URL}json/class_list.json')