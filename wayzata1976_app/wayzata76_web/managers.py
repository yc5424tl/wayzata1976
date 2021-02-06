from .models import Address, Person
import json
import sqlite3
import django.db
from django.db.backends.sqlite3.base import IntegrityError as SQLite3IntegrityError
from django.db.backends.postgresql.base import (
    IntegrityError as PostgreSQLIntegrityError,
)


def build_objects_from_classlist(json_file):
    json_data = json.load(open(json_file))
    for record in json_data:
        try:
            new_person = extract_person(record)
            if new_person:
                new_address = extract_address(record)
                if new_address:
                    new_person.address = new_address
                new_person.save()
        except (PostgreSQLIntegrityError, SQLite3IntegrityError) as iE:
            continue


def extract_address(record):
    try:
        city = record["city"]
        state = record["state"]
        zip_code = record["zip"]
        new_address = Address(city=city, state_province=state, zip_code=zip_code)
        new_address.save()
        return new_address
    except KeyError as kE:
        return None


def extract_person(record):
    try:
        last_name = record["last_name"]
        first_name = record["first_name"]
        middle_initial = record["middle_initial"]
        new_person = Person(
            last_name=last_name, first_name=first_name, middle_initial=middle_initial
        )
        return new_person
    except KeyError as kE:
        return None
    except (PostgreSQLIntegrityError, SQLite3IntegrityError) as iE:
        return None