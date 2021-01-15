from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from wayzata76_web.models import CustomUser, NewsPost, Gallery, GalleryImage, NewsPostImage

import uuid
import requests


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CreateNewsPostForm(forms.ModelForm):
    header = forms.CharField(label='Title')
    body = forms.Textarea()
    image = forms.ImageField(required=False, label='Select Image')

    class Meta:
        model = NewsPost
        fields = ('header', 'body')
        widgets = {
            'body': forms.Textarea(
                attrs = {
                    'height': '60vh',
                    'width': '90%',
                    'overflow-y': 'scroll',
                    'padding': '1em',
                }
            )
        }


class UploadGalleryImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UploadGalleryImageForm, self).__init__(*args, **kwargs)

    title = forms.CharField(required=False, label='title', max_length=100)
    # image = forms.URLField(widget=S3DirectWidget(dest='example_destination')) # TODO update destination

    subtitle = forms.CharField(required=False, label='Subtitle')
    gallery = forms.ModelChoiceField(queryset=Gallery.objects.all())

    class Meta:
        model = GalleryImage
        fields = ('title', 'subtitle', 'gallery', 'image')


class MultiUploadGalleryImageForm(forms.ModelForm):

   gallery = forms.ModelChoiceField(queryset=Gallery.objects.all())

    class Meta:
        model = GalleryImage
        fields = ('image', 'gallery')


class CreateGalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ['working_name', 'display_name']

    working_name = forms.CharField(required=True, max_length=100)
    display_name = forms.CharField(required=True, max_length=100)


# class S3DirectUploadForm(forms.Form):
#         image = forms.URLField(widget=S3DirectWidget(dest='example_destination')) # TODO update destination
