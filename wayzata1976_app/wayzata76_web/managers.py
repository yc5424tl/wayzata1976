
from django.db import models

from django.db.models import Q

class PersonQuerySet(models.QuerySet):

    def classmates(self):
        return self.filter(is_classmate=True).only("last_name", "first_name", "middle_initial", "address", "is_classmate").order_by("last_name").select_related("address")

    def mia(self):
        return self.filter(address=None, is_classmate=True).only("last_name", "first_name", "middle_initial", "address", "is_classmate").order_by("last_name").select_related("address")

    def passed(self):
        return self.filter(address__city="passed").only("last_name", "first_name", "middle_initial", "address", "is_classmate").order_by("last_name").select_related("address")

    def in_contact(self):
        return self.exclude(Q(address__city="passed") | Q(address=None)).order_by("last_name").select_related("address")

class PersonManager(models.Manager):

    def get_queryset(self):
        return PersonQuerySet(self.model, using=self._db)

    def classmates(self):
        return self.get_queryset().classmates()

    def mia(self):
        return self.get_queryset().mia()

    def passed(self):
        return self.get_queryset().passed()

    def in_contact(self):
        return self.get_queryset().in_contact()




