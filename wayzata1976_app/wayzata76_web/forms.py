from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, NewsPost, Gallery, GalleryImage, NewsPostImage, SurveyResult, ContactInfo
from django.conf import settings
from django.urls import reverse
import uuid
import requests
from django.template.loader import render_to_string
import os
from django.utils.translation import ugettext_lazy as _

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class ContactUpdateForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         if self.fields[field].widget.__class__.__name__ in ('AdminTextInputWidget', 'Textarea', 'NumberInput', 'AdminURLFieldWidget', 'Select'):
    #             self.fields[field].widget.attrs.update({
    #                 'class': 'form-control'
    #             })

    first_name = forms.CharField(max_length=100)
    middle_initial = forms.CharField(max_length=10, required=False)
    last_name = forms.CharField(max_length=100)
    street_address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    state_province = forms.CharField(max_length=100, required=False)
    zip_code = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=100, required=False)
    spouse_is_classmate = forms.CheckboxInput()
    spouse_is_alumni = forms.CheckboxInput()
    spouse_first_name = forms.CharField(max_length=100, required=False)
    spouse_middle_initial = forms.CharField(max_length=10, required=False)
    spouse_last_name = forms.CharField(max_length=100, required=False)


    class Meta:
        model = ContactInfo
        fields = ('first_name', 'middle_initial', 'last_name', 'street_address', 'city', 'state_province', 'zip_code', 'country', 'phone', 'email', 'spouse_is_classmate', 'spouse_is_alumni', 'spouse_first_name', 'spouse_middle_initial', 'spouse_last_name')
         # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         if self.fields[field].widget.__class__.__name__ in ('AdminTextInputWidget', 'Textarea', 'NumberInput', 'AdminURLFieldWidget', 'Select'):
    #             self.fields[field].widget.attrs.update({
    #                 'class': 'form-control'
    #             })


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


#  For Adding to Existing News Post
class UploadNewsPostImageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UploadNewsPostImageForm, self).__init__(*args, **kwargs)

    title = forms.CharField(required=False, label='title', max_length=100)
    subtitle = forms.CharField(required=False, label='subtitle', max_length=100)

    class Meta:
        model = NewsPostImage
        fields = ('title', 'subtitle', 'image')


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
        fields = ['working_name', 'display_name', 'abstract_gallery', 'section']
        widgets = {
            'section': forms.Select(choices=Gallery.SECTIONS, attrs={'class': 'form_control'}),
        }

    working_name = forms.CharField(required=True, max_length=100)
    display_name = forms.CharField(required=True, max_length=100)
    abstract_gallery = forms.CheckboxInput()
    section = forms.ChoiceField
    subgallery = forms.CheckboxInput()
    parent_gallery = forms.ModelChoiceField(queryset=Gallery.objects.filter(abstract_gallery=True).all())


# class S3DirectUploadForm(forms.Form):
#         image = forms.URLField(widget=S3DirectWidget(dest='example_destination')) # TODO update destination

class TestUploadForm(forms.ModelForm):

    gallery = forms.ModelChoiceField(queryset=Gallery.objects.all())
    title = forms.CharField(max_length=100, required=False)
    subtitle = forms.CharField(max_length=100, required=False)

    def __init__(self, data=None, files=None, *args, **kwargs):
        super().__init__(data, files, *args, **kwargs)
        self.accept = settings.MY_UPLOAD_FORM_ACCEPT
        self.max_image_size = settings.MY_UPLOAD_FORM_MAX_IMAGE_SIZE
        self.data = data
        self.files = files
        self.file_errors = []
        self.accept = None
        self.max_image_size = 0


    class Meta:
        model = GalleryImage
        fields = ('image', 'gallery', 'title', 'subtitle')

    def form_valid(self, request):
        self.dump()
        files = self.files.getlist('files')
        # title = self.cleaned_data['title']
        # subtitle = self.cleaned_data['subtitle']
        gallery = self.cleaned_data['gallery']

        for i, file in enumerate('files'):
            messages.info(request, '[%d]: "%s" received' % (i, file))
            image = GalleryImage.objects.create(gallery=gallery, uploaded_by=request.user)
            image.file.save(file.name, file)

        return self.get_success_url(request)


    def get_success_url(self, request=None):
        return '/'


    def get_action(self, request=None):
        return reverse('test_upload_form')


    def get_accept(self, request=None):
        """
        Might be overridden
        Example:
            return 'image/*'
        Defaults to: list of allowed file types
        """
        return self.accept


    def as_html(self, request):

        accept = self.get_accept()
        if accept is None:
            accept = ','.join(settings.UPLOAD_FORM_ALLOWED_FILE_TYPES)

        html = render_to_string(
            'upload_form/upload_form.html', {
                'form': self,
                'file_errors': self.file_errors,
                'action': self.get_action(request),
                'accept': accept,
                'max_image_size': self.get_max_image_size(request),
                'UPLOAD_FORM_PARALLEL_UPLOAD': settings.UPLOAD_FORM_PARALLEL_UPLOAD,
            },
            request
        )
        return html


    def dump(self):
        print('=' * 128)
        print(self.data)
        print('-' * 128)
        print(self.files)
        files = self.files.getlist('files')
        for i, file in enumerate(files):
            print('[%d]: "%s"' % (i, file))
        print('=' * 128)


    def get_max_image_size(self, request=None):
        """
        Might be overridden
        """
        return self.max_image_size

    def is_valid(self):

        allowed_file_types = settings.UPLOAD_FORM_ALLOWED_FILE_TYPES
        max_file_size_MB = settings.MY_UPLOAD_FORM_MAX_IMAGE_SIZE

        self.file_errors = []
        files = self.files.getlist('files')
        for file in files:
            name, extension = os.path.splitext(file.name)
            extension = extension.lower()
            size_MB = file.size / (1024 * 1024)
            if extension not in allowed_file_types:
                self.file_errors.append("%s: %s" % (file.name, _('File type not allowed')))
            if size_MB > max_file_size_MB:
                self.file_errors.append("%s: %s" % (file.name, _('File size exceeds %s MB limit') % str(max_file_size_MB)))

        #return len(self.file_errors) <= 0
        valid = super().is_valid() and len(self.file_errors) <= 0
        return valid


        # class SurveyForm(forms.ModelForm):
#     class Meta:
#         model = Survey
#         fields = ['title']

# class QuestionForm(forms.ModelForm):  # to add a question to a survey
#     class Meta:
#         model = Question
#         fields = ['prompt']

# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         widgets =  {
#             'response': question.input_type,
#         }


# class OptionForm(forms.ModelForm):
#     class Meta:
#         model = Option
#         fields = ['text']


# class AnswerForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         options = kwargs.pop('options') # target should be list of options <[opt]>
#         choices = {(o.pk, o.text) for o in options}
#         super().__init__(*args, **kwargs)
#         option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
#         self.fields['options'] = option_field