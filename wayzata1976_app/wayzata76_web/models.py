from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from s3direct.fields import S3DirectField
import uuid
from geopy.geocoders import Nominatim



class Address(models.Model):
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=15, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.city}, {self.state_province} ({self.zip})'


    def geolocate_zip(self, geolocator):
        if self.zip:
            try:
                # geolocator = Nominatim(user_agent='wayzata76_web')
                location = geolacator.geocode(self.zip)

                if location.longitude and location.latitude:
                    self.longitude = location.longitude
                    self.latitude = location.latitude 
                    self.save()
                    return True
                return False
            except:
                print('exception in geolocate_zip')
                return False


class Gallery(models.Model):
    working_name = models.CharField(max_length=100, null=False, blank=False)
    display_name = models.CharField(max_length=100, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.display_name

    @property
    def readable_date_created(self):
        return f'{self.date_created.month}, {self.date_created.day}, {self.date_created.year}'


class Image(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_related',
        related_query_name="%(app_label)s_%(class)ss",
        )
    subtitle = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title} - {self.date_created} ({self.uploader})'


def gallery_for_image(instance, filename):
    name, ext = filename.split('.')
    # file_path = f'{instance.gallery.working_name}/{name}.{ext}'
    file_path = f'{instance.gallery.working_name}/{instance.uuid}.{ext}'
    return file_path


class GalleryImage(Image):
    gallery = models.ForeignKey(Gallery, on_delete=models.PROTECT, related_name='gallery_images')
    # image = S3DirectField(dest='example_destination') # TODO update destination
    image = models.ImageField(upload_to=gallery_for_image)


class NewsPost(models.Model):
    header = models.CharField(max_length=100, null=False, blank=False)
    body = models.CharField(max_length=5000, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)


class NewsPostImage(Image):
    news_post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='news_post_image')


class Person(models.Model):
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.PROTECT, related_name='people')
    last_name = models.CharField(max_length=100, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_initial = models.CharField(max_length=1, null=True, blank=True, default=None)
    nickname = models.CharField(max_length=100, null=True, blank=True, default=None)
    phone = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    is_classmate= models.BooleanField(default=True)
    is_alumni = models.BooleanField(default=False)
    is_relative = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, default=None, on_delete=models.PROTECT)


class SurveyResult(models.Model):
    liked = models.CharField(max_length=1000, null=True, blank=True)
    disliked = models.CharField(max_length=1000, null=True, blank=True)
    location_idea = models.CharField(max_length=1000, null=True, blank=True)
    music_idea = models.CharField(max_length=1000, null=True, blank=True)
    misc_idea = models.CharField(max_length=1000, null=True, blank=True)
    submitted_by = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def has_form_field(self, field_name):
        try:
            return (True, bool(getattr(self, field_name).strip()))  #  True indicates the field exists, bool() to check that the field is not None or empty
        except:
            return (False, False)  # First False indicates field does not exist, Second that there is no data being returned for the target field

    def has_content(self):
        for field_name in ['liked', 'disliked', 'location_idea', 'music_idea', 'misc_idea', 'submitted_by', 'email']:
            if self.has_form_field(field_name):
                return True
        return False

    @property
    def readable_date_created(self):
        return f'{self.date_created.month}, {self.date_created.day}, {self.date_created.year}'


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username