import os
import uuid
import pytz

import requests
from django.utils.translation import ugettext_lazy as _
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


from .models import (
    ContactInfo,
    CustomUser,
    Gallery,
    GalleryImage,
    NewsPost,
    NewsPostImage,
    SurveyResult,
    HomepagePost,
    HomepagePostImage,
)

from tinymce.widgets import TinyMCE



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class QuestionnaireForm(forms.ModelForm):

    MUSIC_CHOICES = [
        ('band', 'Live Band'),
        ('dj', 'Professional DJ'),
        ('karaoke', 'Karaoke'),
        ('playlist', 'Playlist of 70\'s music'),
        ('other', 'Other')
    ]

    music = forms.ChoiceField(choices=MUSIC_CHOICES, label="What would you choose for musical enjoyment?")
    submitted_by = forms.CharField(required=True, max_length=100)
    email = forms.CharField(required=True, max_length=100)

    class Meta:
        model = SurveyResult
        exclude = ['date_created']
        labels = {
            'liked': _('If you attended the 40th reunion, what did you like most about it?'),
            'disliked': _('If you attended the 40th reunion, what would you have changed to make it better?'),
            'location': _('Where would you like the 45th reunion to be held?'),
            'music': _('What would you choose for musical enjoyment?'),
            'food': _('What kind of food would you like to have available?'),
            'misc': _('Other questions, comments, suggestions, recommendations, or cryptic messages?'),
            'submitted_by': _('Name'),
        }
        widgets = {
            'liked': forms.widgets.Textarea(attrs={'cols':80, 'rows': 10}),
            'disliked': forms.widgets.Textarea(attrs={'cols':80, 'rows': 10}),
            'location': forms.widgets.Textarea(attrs={'cols':80, 'rows': 10}),
            'music_other': forms.widgets.Textarea(attrs={'cols':80, 'rows': 10}),
            'food': forms.widgets.Textarea(attrs={'cols':80, 'rows': 10}),
            'misc': forms.widgets.Textarea(attrs={'cols':80, 'rows': 10}),
        }


    def has_value(self, field):
        try:
            return bool(
                getattr(self, field).strip()
            )
        except:
            return False

    def has_content(self):
        field_checks = [
            self.fields['liked'],
            self.fields['disliked'],
            self.fields['location'],
            self.fields['food'],
            self.fields['misc'],
            self.fields['submitted_by'],
            self.fields['email']
        ]
        for field in field_checks:
            if self.has_value(field):
                return True
        return False



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
        widgets = {
            "first_name": forms.TextInput(attrs={"autocomplete":"given-name"}),
            "middle_initial": forms.TextInput(attrs={"autocomplete":"additional-name"}),
            "last_name": forms.TextInput(attrs={"autocomplete":"family-name"}),
            "street_address": forms.TextInput(attrs={"autocomplete":"street-address"}),
            "city": forms.TextInput(attrs={'autocomplete': 'address-level1'}),
            "state_province": forms.TextInput(attrs={'autocomplete': 'address-level2'}),
            "zip_code": forms.TextInput(attrs={'autocomplete': 'postal-code'}),
            "country": forms.TextInput(attrs={'autocomplete': 'country'}),
            "phone": forms.TextInput(attrs={'autocomplete': 'tel'}),
            "email": forms.EmailInput(attrs={'autocomplete': 'email'}),
        }


class HomepagePostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(HomepagePostForm, self).__init__(*args, **kwargs)

    title = forms.CharField(max_length=500, required=True)
    subtitle = forms.CharField(max_length=500, required=False)
    footnote = forms.CharField(max_length=500, required=False)
    body=forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}), max_length=20000, required=False)

    class Meta:
        model = HomepagePost
        exclude = ['author', 'date_created']
        labels = {'active': 'Publish Now: ' }


class HomepagePostImageForm(forms.ModelForm):
    class Meta:
        model = HomepagePostImage
        fields = ['image', 'caption']
        labels = {'image': 'Upload Image: '}


class NewsPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(NewsPostForm, self).__init__(*args, **kwargs)

    header = forms.CharField(max_length=100, required=True)
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}), max_length=5000, required=False)

    class Meta:
        model = NewsPost
        fields = ('body', 'header')


class NewsPostImageForm(forms.ModelForm):
    class Meta:
        model = NewsPostImage
        fields = ['image', 'subtitle']
        labels = {'image': 'Upload Image'}


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
    return ((x.id, x.display_name) for x in GalleryImageForm.GALLERY_OPTIONS)



class GalleryImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(GalleryImageForm, self).__init__(*args, **kwargs)

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
                "autocomplete": "username",
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
                "autocomplete": "password",
            }
        )
    )
