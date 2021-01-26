from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import GalleryImage, Person, CustomUser, NewsPostImage, SurveyResult, ContactInfo, NewsPost, Yearbook, Gallery
from .forms import UploadGalleryImageForm, CustomUserCreationForm, MultiUploadGalleryImageForm, UploadNewsPostImageForm, TestUploadForm, ContactUpdateForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
import os
import json
import string

# class UploadImageS3(FormView):
#     template_name = 's3_direct_upload.html'
#     form_class = S3DirectUploadForm


def SignUpView(CreateView):
    form_class = CustomUserCreationForm
    succes_url = reverse_lazy('login')
    template_name = 'registration.signup.html'


# def login(request):
#     if request.method == 'GET':
#         return render('registration/login.html')
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             return redirect('login')

def index(request):
    return render(template_name='index.html', request=request)


def upcoming(request):
    pass


def questionnaire(request):
    if request.method == 'POST':
        liked = request.POST['liked']
        disliked = request.POST['disliked']
        location = request.POST['location']
        music = request.POST['music']
        music_other = request.POST['music_other']
        misc = request.POST['misc']
        submitted_by = request.POST['name']
        email = request.POST['email']

        new_result = SurveyResult(
            liked=liked, disliked=disliked, location=location, music=music, music_other=music_other, misc=misc, submitted_by=submitted_by, email=email
        )
        if new_result.has_content:
            new_result.save()
            messages.success(request, 'Thank you, your questionnaire has been submitted!')
            return render(request, 'main/index.html')
        else:
            new_result.delete()
            messages.warning(request, 'A blank questionnaire cannot be submitted, please try again.')
            return render(request, 'main/questionnaire.h{% block content %}tml')
    else:
        return render(request, 'main/questionnaire.html')


def contact_info(request):
    if request.method == 'POST':
        form = ContactUpdateForm(request.POST)
        if form.is_valid():
            contact_info = form.save(commit=False)
            if request.user.is_authenticated:
                contact_info.user = request.user
            contact_info.save()
            messages.success(request, 'Updated contact information has been submitted. Thank you.')
            # TODO - if submitter is logged in user, check to see if user is attatched to a person -- update corresponding fields 
            # TODO - check if all Address fields contain data, create new Address if so, linking it to Person
            # TODO - check Person for matching first/last name, creating a new entry if they do not -- same for spouse fields 
            return redirect('success')
        else:
            message = ''
            for error in form.errors:
                message += f'{error}: {form.errors[error]}\n'
            messages.warning(request, message)
    else:
        form = ContactUpdateForm()
        # TODO -- if request.user.is_authenticated --> prefill email/name/address on form 
    return render(request, 'main/contact_update.html', {'form': form})


def view_gallery(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    return render(request, 'main/view_gallery.html', {'gallery': gallery })



def view_zietgeist(request):
    awards =[
        {'award': 'Best Picture', 'winner': 'Rocky'},
        {'award': 'Best Actor', 'winner': 'Peter Finch (Network)'},
        {'award': 'Best Actress', 'winner': 'Faye Dunaway (Network)'},
        {'award': 'Best Supporting Actor', 'winner': 'Jason Robards (All the President\'s Men)'},
        {'award': 'Best Supporting Actress', 'winner': 'Beatrice Straight (Network)'},
        {'award': 'Best Director', 'winner': 'John Avildsen (Rocky)'}
    ]
    yearbooks = Yearbook.objects.all()
    songs = None
    with open(os.path.join(settings.STATIC_ROOT, 'json/songs.json')) as file:
        songs = json.load(file)
    return render(request, 'main/zietgeist.html', {'yearbooks': yearbooks, 'songs': songs, 'awards': awards})


def view_classmates(request):

    classmates = Person.objects.filter(is_classmate=True).only('last_name', 'first_name', 'middle_initial', 'address', 'is_classmate').order_by('last_name').select_related('address')
    mia_list = Person.objects.filter(address=None, is_classmate=True).only('last_name', 'first_name', 'middle_initial', 'address', 'is_classmate').order_by('last_name').select_related('address')
    passed_list = Person.objects.filter(address__city='passed').only('last_name', 'first_name', 'middle_initial', 'address', 'is_classmate').order_by('last_name').select_related('address')
    in_contact_list = Person.objects.exclude(Q(address__city='passed') | Q(address=None)).order_by('last_name').select_related('address')

    alphabet = list(string.ascii_uppercase)

    all_link_dict = {letter:None for letter in alphabet}
    for letter_key in all_link_dict:
        if letter_key == 'X':
            continue
        else:
            for classmate in classmates:
                if classmate.last_name[0] ==  letter_key:
                    all_link_dict[letter_key] = classmate
                    break

    mia_link_dict =  {letter:None for letter in alphabet}
    for letter_key in mia_link_dict:
        if letter_key in ['X', 'Q', 'U', 'X', 'Y', 'Z']:
            continue
        else:
            for classmate in mia_list:
                if classmate.last_name[0] == letter_key:
                    mia_link_dict[letter_key] = classmate
                    break

    in_c_link_dict = {letter:None for letter in alphabet}
    for letter_key in in_c_link_dict:
        if letter_key in ['I', 'U', 'X']:
            continue
        else:
            for classmate in in_contact_list:
                if classmate.last_name[0] == letter_key:
                    in_c_link_dict[letter_key] = classmate
                    break

    return render(request, 'main/view_classmates.html', {
        'classmates': classmates,
        'mia_list': mia_list,
        'passed_list': passed_list,
        'in_contact_list': in_contact_list,
        'link_dict': all_link_dict,
        'mia_link_dict': mia_link_dict,
        'in_c_link_dict': in_c_link_dict,
        'alphabet': alphabet
        }
    )

class ClassmateList(ListView):
    template_name = 'main/view_classmates.html'
    paginate_by = 50
    context_object_name = 'classmates'

    def get_queryset(self):
        self.queryset = Person.objects.filter(address=None).only('last_name', 'first_name', 'middle_initial', 'address', 'is_classmate').order_by('last_name').select_related('address')
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(ClassmateList, self).get_context_data(**kwargs)
        context['classmates'] = self.queryset
        context['mia_list'] = Person.objects.filter(address=None).only('last_name', 'first_name', 'middle_initial', 'address', 'is_classmate').order_by('last_name').select_related('address')
        context['passed_list'] = Person.objects.filter(address__city='passed').only('last_name', 'first_name', 'middle_initial', 'address', 'is_classmate').order_by('last_name').select_related('address')
        context['in_contact_list'] = Person.objects.exclude(address__city='passed', address=None).order_by('last_name').select_related('address')
        return context


def view_links(request):
    pass


def view_contact(request):
    pass


def view_news(request):
    posts = NewsPost.objects.all()
    return render(request, 'main/view_news.html', {'posts': posts})


def view_galleries(request):
    pass


def create_news_post(request):
    pass


def upload_news_post_image(request):
    if request.method == 'POST':
        form = UploadNewsPostImageForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            news_post_image = form.save(commit=False)
            news_post_image.uploaded_by = request.user
            news_post_image.save()
            return redirect('success')
    else:
        form = UploadNewsPostImageForm()
        # user = CustomUser(pk=request.user.pk)
        uploaded_news_post_images = request.user.news_post_images.all()
        uploaded_gallery_images = request.user.gallery_images.all()
        return render(request, 'upload/upload_news_post_image.html', {'form': form, 'news_post_images': uploaded_news_post_images, 'gallery_images': uploaded_gallery_images})


def upload_gallery_image(request):
    if request.method == 'POST':
        form = UploadGalleryImageForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            gallery_image = form.save(commit=False)
            gallery_image.uploaded_by = request.user
            gallery_image.save()
            return redirect('success')
    else:
        form = UploadGalleryImageForm()
    return render(request, 'upload/local_image_upload.html', {'form': form})


def multi_upload_gallery_image(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            form = MultiUploadGalleryImageForm()
            prior_uploads = request.user.gallery_images.all()
        return render(request, 'upload/multi_upload_gallery_image_form.html', {'prior_uploads': prior_uploads, 'form': form})
    elif request.method == 'POST':
        form = MultiUploadGalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'title': photo.image.title, 'url': photo.image.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)



def success(request):
    return HttpResponse('successfully uploaded')


def multi_upload_test(request, gallery):
    if request.method == 'POST':
        for file in request.FILES.getlist('images'):
            instance = GalleryImage(
                gallery={{ gallery }},
                image=file,
                uploaded_by=request.user
                )
            instance.save()

    else:
        return render(request, 'upload/multi_upload_test.html')


# class TestUploadForm(UploadForm):

#     def form_valid(self, request):
#         self.dump()
#         return self.get_success_url(request)

#     def get_success_url(self, request=None):
#         return '/'

#     def get_action(self, request=None):
#         return reverse('test_view')

def test_view(request):
    if request.method == 'GET':
        form = TestUploadForm()
    else:
        form = TestUploadForm(request.POST, request.FILES)
        if form.is_valid():
            url = form.form_valid(request)
            return JsonResponse({'action': 'redirect', 'url': url, })
        else:
            return JsonResponse({'action': 'replace', 'html': form.as_html(request), })
    return render(
        request, 'test_view.html', {
            'form': form,
            'form_as_html': form.as_html(request),
        }
    )

def my_upload_target_view(request):
    if request.method == 'POST' and request.is_ajax():
        form = TestUploadForm(request.POST, request.FILES)

        if form.is_valid():
            url = form.form_valid(request)
            return JsonResponse({'action': 'redirect', 'url': url, })
        else:
            return JsonResponse({'action': 'replace', 'html': form.as_html(request), })
    return render(request, 'test_view.html', {'form': form, 'form_as_html': form.as_html(request)} )