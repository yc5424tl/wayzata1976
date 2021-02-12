import os
import uuid
import pytz

import requests
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .models import (
    ContactInfo,
    CustomUser,
    Gallery,
    GalleryImage,
    NewsPost,
    NewsPostImage,
    SurveyResult,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class ContactUpdateForm(forms.ModelForm):

    COUNTRY_CHOICES = [(k,pytz.country_names[k]) for k in pytz.country_names]

    first_name = forms.CharField(max_length=100)
    middle_initial = forms.CharField(max_length=10, required=False)
    last_name = forms.CharField(max_length=100)
    street_address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    state_province = forms.CharField(max_length=100, required=False)
    zip_code = forms.CharField(max_length=15, required=False)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, initial=('US', 'United States'), required=False)
    phone = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=100, required=False)
    spouse_is_classmate = forms.CheckboxInput()
    spouse_is_alumni = forms.CheckboxInput()
    spouse_first_name = forms.CharField(max_length=100, required=False)
    spouse_middle_initial = forms.CharField(max_length=10, required=False)
    spouse_last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = ContactInfo
        fields = (
            "first_name",
            "middle_initial",
            "last_name",
            "street_address",
            "city",
            "state_province",
            "zip_code",
            "country",
            "phone",
            "email",
            "spouse_is_classmate",
            "spouse_is_alumni",
            "spouse_first_name",
            "spouse_middle_initial",
            "spouse_last_name",
        )


class NewsPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(NewsPostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = NewsPost

        fields = (
            "link",
            "link_text",
            "body",
            'header'
        )
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "height": "60vh",
                    "width": "90%",
                    "overflow-y": "scroll",
                    "padding": "1em",
                }
            )
        }


class ExtendedNewsPostForm(NewsPostForm):

    image = forms.ImageField(allow_empty_file=True, required=False, label="Image (opt.)")
    subtitle = forms.CharField(max_length=100, required=False)

    class Meta(NewsPostForm.Meta):
        fields = NewsPostForm.Meta.fields + ('image', 'subtitle', )


#  For Adding to Existing News Post
class UploadNewsPostImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UploadNewsPostImageForm, self).__init__(*args, **kwargs)

    title = forms.CharField(required=False, label="title", max_length=100)
    subtitle = forms.CharField(required=False, label="subtitle", max_length=100)

    class Meta:
        model = NewsPostImage
        fields = ("image",)


class UploadGalleryImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(UploadGalleryImageForm, self).__init__(*args, **kwargs)


    title = forms.CharField(required=False, label="title", max_length=100)
    subtitle = forms.CharField(required=False, label="Subtitle")

    class Meta:
        model = GalleryImage

        fields = (
            "image",
            "gallery",
        )
        widgets = {
            "gallery": forms.Select(
                choices=Gallery.objects.all().filter(abstract_gallery=False),
                attrs={"class": "form-control"},
            ),
        }

class CreateGalleryForm(forms.ModelForm):

    working_name = forms.CharField(required=True, max_length=100)
    display_name = forms.CharField(required=True, max_length=100)
    subgallery = forms.CheckboxInput()
    parent_gallery = forms.ModelChoiceField(
        queryset=Gallery.objects.filter(abstract_gallery=True).all()
    )

    class Meta:
        model = Gallery
        fields = (
            "abstract_gallery",
            "section",
        )
        widgets = {
            "section": forms.Select(
                choices=Gallery.SECTIONS, attrs={"class": "form_control"}
            ),
        }


def gallery_choices():
    return ((x.id, x.display_name) for x in GalleryImageUploadForm.GALLERY_OPTIONS)


class GalleryImageUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(GalleryImageUploadForm, self).__init__(*args, **kwargs)

    image = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

    class Meta:
        model = GalleryImage
        fields = ("gallery",)
        widgets = {
            "gallery": forms.Select(
                choices=Gallery.objects.all().filter(abstract_gallery=False)
            )
        }


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm mr-sm-2",
                "type": "text",
                "placeholder": "username",
                "aria-label": "username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-sm mr-sm-2",
                "type": "password",
                "placeholder": "password",
                "aria-label": "password",
            }
        )
    )
