from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from s3direct.fields import S3DirectField
import uuid
from geopy.geocoders import Nominatim
from django import forms
from .storage_backends import PublicMediaStorage
import pytz

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Address(models.Model):
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=15, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.state_province} ({self.zip_code})"

    def geolocate_zip(self, geolocator):
        if self.zip_code:
            try:
                locator = geolocator
                # geolocator = Nominatim(user_agent='wayzata76_web')
                location = locator.geocode(self.zip)

                if location.longitude and location.latitude:
                    self.longitude = location.longitude
                    self.latitude = location.latitude
                    self.save()
                    return True
                return False
            except:
                return False


class Gallery(models.Model):

    SECTIONS = (
        ("REUNIONS", "Reunions"),
        ("STUDENT_LIFE", "Student Life"),
        ("STOMPING_GROUNDS", "The Stomping Grounds"),
    )

    working_name = models.CharField(max_length=100, null=False, blank=False)
    display_name = models.CharField(max_length=100, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(default=None, null=True, blank=True)
    section = models.TextField(choices=SECTIONS, null=True, blank=False)
    abstract_gallery = models.BooleanField(default=False)
    subgallery = models.BooleanField(default=False)
    parent_gallery = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="sub_galleries",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.display_name

    @property
    def has_subgalleries(self):
        return self.sub_galleries.exists()

    @property
    def readable_date_created(self):
        return f"{self.date_created.month}, {self.date_created.day}, {self.date_created.year}"


class Image(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    # uploaded_by = models.ForeignKey(
    # settings.AUTH_USER_MODEL,
    # on_delete=models.PROTECT,
    # related_name = 'images')
    # related_name='%(app_label)s_%(class)s_related',
    # related_query_name="%(app_label)s_%(class)ss",
    # )
    subtitle = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title} - {self.date_created} ({self.uploaded_by})"


def remove_extra_periods(target_str):
    for period in range(target_str.count('.')-1):
        for x in target_str:
            if x == '.':
                if target_str.find(x) != target_str.rfind(x):
                    target_str = target_str.replace(x, '_', 1)
    return target_str
    
def gallery_for_image(instance, filename):
    cleaned_filename = remove_extra_periods(filename)
    name, ext = cleaned_filename.replace(' ', '_').split(".")
    file_path = f"{instance.gallery.working_name}/{instance.uuid}.{ext}"
    return file_path


class GalleryImage(Image):
    gallery = models.ForeignKey(
        Gallery, on_delete=models.PROTECT, related_name="gallery_images"
    )
    image = models.ImageField(
        storage=PublicMediaStorage, upload_to=gallery_for_image, null=True, blank=False
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="gallery_images",
    )


class NewsPost(models.Model):
    header = models.CharField(max_length=100, null=False, blank=False)
    body = models.CharField(max_length=5000, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    link = models.URLField(null=True, blank=True)
    link_text = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ["-date_created"]


def news_post_image_path(instance, filename):
    name, ext = filename.split(".")
    file_path = f"news_post_image/{instance.uuid}.{ext}"
    return file_path


class NewsPostImage(Image):
    news_post = models.OneToOneField(
        NewsPost, on_delete=models.CASCADE, related_name="news_post_image"
    )
    image = models.ImageField(
        storage=PublicMediaStorage,
        upload_to=news_post_image_path,
        null=True,
        blank=True,
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="news_post_images",
    )

    def __name__(self):
        return "news_post_image"


class Person(models.Model):
    address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.PROTECT, related_name="people"
    )
    last_name = models.CharField(max_length=100, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_initial = models.CharField(max_length=10, null=True, blank=True, default=None)
    nickname = models.CharField(max_length=100, null=True, blank=True, default=None)
    phone = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    is_classmate = models.BooleanField(default=True)
    is_alumni = models.BooleanField(default=False)
    is_relative = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return (
            f"{self.first_name} {self.middle_initial} {self.last_name}, {self.address}"
        )


class ContactInfo(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    middle_initial = models.CharField(max_length=10, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_province = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    # country = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=2, choices=pytz.country_names.items(), null=True, blank=True, default=None)
    phone = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    spouse_is_classmate = models.BooleanField(default=False)
    spouse_is_alumni = models.BooleanField(default=False)
    spouse_first_name = models.CharField(max_length=100, null=False, blank=False)
    spouse_middle_initial = models.CharField(max_length=10, null=True, blank=True)
    spouse_last_name = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        default=None,
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"First Name: {self.first_name}\nMiddle: {self.middle_initial if self.middle_initial else '--'}\nLast Name: {self.last_name}\nStreet Address: {self.street_address if self.street_address else '--'}\nCity: {self.city if self.city else '--'}\nState/Province: {self.state_province if self.state_province else '--'}\nZip Code: {self.zip_code if self.zip_code else '--'}\nCountry: {self.country if self.country else '--'}\nPhone: {self.phone if self.phone else '--'}\nEmail: {self.email if self.email else '--'}\nSpouse is Classmate: {self.spouse_is_classmate}\nSpouse is Alumni: {self.spouse_is_alumni}\nSpouse First Name: {self.spouse_first_name if self.spouse_first_name else '--'}\nSpouse Middle: {self.spouse_middle_initial if self.spouse_middle_initial else '--'}\nSpouse Last Name: {self.spouse_last_name if self.spouse_last_name else '--'}\nSubmitted by: {self.user.username if self.user else 'Anonymous'}"


class SurveyResult(models.Model):
    liked = models.CharField(max_length=1000, null=True, blank=True)
    disliked = models.CharField(max_length=1000, null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)
    music = models.CharField(max_length=1000, null=True, blank=True)
    music_other = models.CharField(max_length=1000, null=True, blank=True)
    misc = models.CharField(max_length=1000, null=True, blank=True)
    submitted_by = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def has_form_field(self, field_name):
        try:
            return bool(
                getattr(self, field_name).strip()
            )  #  True indicates the field exists, bool() to check that the field is not None or empty
        except:
            return False  # First False indicates field does not exist, Second that there is no data being returned for the target field

    def has_content(self):
        for field_name in [
            "liked",
            "disliked",
            "location",
            "music",
            "music_other",
            "misc",
            "submitted_by",
            "email",
        ]:
            if self.has_form_field(field_name):
                return True
        return False

    @property
    def readable_date_created(self):
        return f"{self.date_created.month}, {self.date_created.day}, {self.date_created.year}"


def yearbook_cover_path(instance, filename):
    name, ext = filename.split(".")
    file_path = f"yearbooks/cover/{instance.uuid}.{ext}"
    return file_path


class Yearbook(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.CharField(max_length=100, null=False, blank=False)
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    cover = models.ImageField(upload_to=yearbook_cover_path)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name="yearbooks",
    )
    gallery = models.OneToOneField(
        Gallery,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="yearbook",
    )
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def display_name(self):
        return f"{self.school} ({self.year})"

    @property
    def working_name(self):
        return f"{self.school}_{self.year}"
