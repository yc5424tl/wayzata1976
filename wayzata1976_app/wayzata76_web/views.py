import json
import os
import string
from urllib.request import urlopen

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import (BadHeaderError, EmailMultiAlternatives,
                              mail_admins, send_mail)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import (ContactUpdateForm, CustomUserCreationForm,
                    GalleryImageForm, HomepagePostForm, HomepagePostImageForm,
                    NewsPostForm, NewsPostImageForm, QuestionnaireForm)  # GalleryImageForm

from .models import (ContactInfo, CustomUser, Gallery, GalleryImage,
                     HomepagePost, HomepagePostImage, NewsPost, NewsPostImage,
                     Person, Song, SurveyResult, Yearbook)


def SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration.signup.html"
    return render


def login(request):
    if request.method == "GET":
        return render(request, "registration/login.html", {})
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "Login Successful")
            return redirect("index")
        else:
            messages.info(request, "Username/Password Incorrect")
            return redirect("index")


def index(request):
    try:
        homepage = HomepagePost.objects.get(active=True)
    except ObjectDoesNotExist:
        homepage = None
    return render(template_name="main/index.html", context={'homepage': homepage}, request=request)


def email_questionnaire_notification(request, survey_result_instance):
    try:
        email_message = f'New Questionnaire Submission:\n\n\
                        Date:                     {survey_result_instance.readable_date_created}\n\
                        Submitted By:             {survey_result_instance.submitted_by if survey_result_instance.submitted_by else "--"}\n\
                        Email:                    {survey_result_instance.email if survey_result_instance.email else "--"}\n\
                        Previous Positive:        {survey_result_instance.liked if survey_result_instance.liked else "--"}\n\
                        Previous Negative:        {survey_result_instance.disliked if survey_result_instance.disliked else "--"}\n\
                        Preferred Location:       {survey_result_instance.location if survey_result_instance.location else "--"}\n\
                        Musical Entertainment:    {survey_result_instance.music if survey_result_instance.music else "--"}\n\
                        Alt Music Entertainment:  {survey_result_instance.music_other if survey_result_instance.music_other else "--"}\n\
                        Food Preferences:         {survey_result_instance.food if survey_result_instance.food else "--"}\n\
                        Misc/Other:               {survey_result_instance.misc if survey_result_instance else "--"}\n\n\
                        wayzata76.com\n\
                        ___________________________________________________________________________________________________\n\
                        Automatically Generated Email - DO NOT REPLY\n'

        email_subject = 'ADMIN: New Questionnaire Submission Received'
        send_mail(email_subject, email_message, 'wayzata1976@gmail.com', ['jkboline@gmail.com', 'wayzata1976@gmail.com'])
        return True

    except:
        return False


def questionnaire(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid() and form.has_content():
                new_survey_result = form.save()
                email_sent = email_questionnaire_notification(request, new_survey_result)
                if email_sent:
                    messages.info(request, "Questionnaire Submitted Successfully. Thank You!")
                else:
                    messages.info(request, "Questionnaire Submitted Successfully. Error Delivering Data to Administration. If the problem persists, please contact us @ wayzata1976.admin@google.com")
                return render(request, "main/index.html")
        else:
            messages.info(request, 'Failure: Empty Form')
            return render(request, 'main/questionnaire.html', {'form': form})
    else:
        form = QuestionnaireForm()
        return render(request, 'main/questionnaire.html', {'form': form})


def email_contact_update_notification(request, contact_info_instance):
    try:
        email_msg = f'A contact information update form has been submitted:\n\n{contact_info_instance}\n\nPlease review the data. To update/add a Person/Address, please use the admin panel (wayzata76.herokuapp.com/admin).\n\nAutomatically Generated Email - Do Not Reply\nwayzata76.com'
        email_subject = 'ADMIN: Contact Form Submission Received -- Review Required'
        send_mail(email_subject, email_msg, 'wayzata1976@gmail.com', ['jkboline@gmail.com', 'wayzata1976@gmail.com'])
        return True
    except:
        return False


def update_contact_info(request):
    if request.method == "POST":
        form = ContactUpdateForm(request.POST)
        if form.is_valid():
            contact_info = form.save(commit=False)
            if request.user.is_authenticated:
                contact_info.user = request.user
            contact_info.save()

            email_sent = email_contact_update_notification(request=request, contact_info_instance=contact_info)
            if email_sent:
                messages.info(request, "Updated contact information has been submitted. Please allow 1-2 days for updates to be approved and applied. Thank you.")
            else:
                messages.info(request, "Updated Contact Information Submitted Successfully, Error Delivering Data to Administration. If the problem persists, please contact us @ wayzata1976.admin@gmail.com")
            return redirect('index')
            # TODO - if submitter is logged in user, check to see if user is attached to a person -- update corresponding fields
            # TODO - migrate address out of contact info, used a combined form in place of this one ---> +1 for creating new addresses and not having crap code
    else:
        form = ContactUpdateForm()
        # TODO -- if request.user.is_authenticated --> prefill email/name/address on form
    return render(request, "main/contact_update.html", {"form": form})


def check_null_empty(target:str) -> str or None:
    if (target is None) or (target.replace(' ', '') == '') :
        return None
    else:
        return target


def update_homepage(request):
    from .forms import HomepagePostImageForm
    if request.method == 'POST':

        homepage_post_form = HomepagePostForm(request.POST)
        homepage_post_image_form = HomepagePostImageForm(request.POST, request.FILES)

        if homepage_post_form.is_valid():

            if homepage_post_form.cleaned_data.get('active'):
                HomepagePost.objects.filter(active=True).update(active=False)
            new_homepage_post = homepage_post_form.save(commit=False)
            new_homepage_post.author = request.user
            new_homepage_post.save()

            if homepage_post_image_form.is_valid():
                if homepage_post_image_form.cleaned_data.get('image'):
                    new_homepage_post_image = homepage_post_image_form.save(commit=False)
                    new_homepage_post_image.homepage_post = new_homepage_post
                    new_homepage_post_image.uploaded_by = request.user
                    new_homepage_post_image.save()

            messages.info(request, 'New Homepage Content Saved')
            return redirect("index")

        homepage_post_form = HomepagePostForm()
        homepage_post_image_form = HomepagePostImageForm()
        messages.info(request, 'Error: Form Contains Invalid Field(s)')
        return render(request, "main/create_homepage_post.html", {'homepage_post_form': homepage_post_form,
                                                                      'homepage_post_image_form': homepage_post_image_form})
    else:
        try:
            homepage_post_form = HomepagePostForm(instance=HomepagePost.objects.filter(active=True).first())
        except ObjectDoesNotExist:
            homepage_post_form = HomepagePostForm()
        try:
            homepage_post = HomepagePost.objects.get(active=True)
            homepage_post_image = homepage_post.homepage_post_image
            image_form = HomepagePostImageForm(instance=homepage_post_image)
        except ObjectDoesNotExist:
            image_form = HomepagePostImageForm()
        # homepage_post_image_form = HomepagePostImageForm()
        return render(request, "main/create_homepage_post.html", {'homepage_post_form': homepage_post_form, 'homepage_post_image_form': image_form})



def view_gallery(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    images = gallery.gallery_images.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(images, 30)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'main/view_gallery.html', {'page_obj': page_obj, 'gallery': gallery, 'paginator': paginator})


def view_zietgeist(request):
    awards = [
        {"award": "Best Picture", "winner": "Rocky"},
        {"award": "Best Actor", "winner": "Peter Finch (Network)"},
        {"award": "Best Actress", "winner": "Faye Dunaway (Network)"},
        {"award": "Best Supporting Actor", "winner": "Jason Robards (All the President's Men)"},
        {"award": "Best Supporting Actress", "winner": "Beatrice Straight (Network)"},
        {"award": "Best Director", "winner": "John Avildsen (Rocky)"},
    ]
    yearbooks = Yearbook.objects.all()
    songs = Song.objects.order_by('position')

    if os.getenv('USE_S3') == 'TRUE':
        json_file = urlopen(static('json/songs.json'))
    else:
        json_file = staticfiles_storage.open('json/songs.json')

    return render(
        request,
        "main/view_zietgeist.html",{"yearbooks": yearbooks, "songs": songs, "awards": awards},
    )


def build_classmate_nav(person_instance_list, ignored_letter_list, alphabet):

    link_dict = {letter: None for letter in alphabet}
    for letter_key in link_dict:
        if letter_key in ignored_letter_list:
            continue
        else:
            for classmate in person_instance_list:
                if classmate.last_name[0] == letter_key:
                    link_dict[letter_key] = classmate
                    break
    return link_dict


def view_classmates(request):

    classmates = Person.people.classmates()
    mia_list = Person.people.mia()
    passed_list = Person.people.passed()
    in_contact_list = Person.people.in_contact()

    no_target_all = ['X']
    no_target_mia = ['X', 'Q', 'U', 'X', 'V', 'Z']
    no_target_passed = ['A', 'G', 'I', 'J', 'K', 'N', 'O', 'Q', 'R', 'U', 'V', 'W', 'X', 'Y', 'Z']
    no_target_in_c = ['I', 'U', 'X']
    #  Create a dictionary with null values to be replaced by the first student (alphabetically) for each letter, the resulting dictionary contains the Person objects to be targeted with anchor links in the classmates list jump menu.

    alphabet = list(string.ascii_uppercase)

    all_link_dict = build_classmate_nav(classmates, no_target_all, alphabet)
    mia_link_dict = build_classmate_nav(mia_list, no_target_mia, alphabet)
    passed_link_dict = build_classmate_nav(passed_list, no_target_passed, alphabet)
    in_c_link_dict = build_classmate_nav(in_contact_list, no_target_in_c, alphabet)

    return render(
        request,
        "main/view_classmates.html",
        {
            "classmates": classmates,
            "mia_list": mia_list,
            "passed_list": passed_list,
            "in_contact_list": in_contact_list,
            "link_dict": all_link_dict,
            "mia_link_dict": mia_link_dict,
            "in_c_link_dict": in_c_link_dict,
            'passed_link_dict': passed_link_dict,
            "no_target_all": no_target_all,
            "no_target_mia": no_target_mia,
            "no_target_passed": no_target_passed,
            "no_target_in_c": no_target_in_c,
            "alphabet": alphabet,
        },
    )


def view_news(request):
    posts = NewsPost.objects.all()
    return render(request, "main/view_news.html", {"posts": posts})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_news_post(request):
    if request.method == "POST":

        news_post_form = NewsPostForm(request.POST)
        news_post_image_form = NewsPostImageForm(request.POST, request.FILES)

        if news_post_form.is_valid():
            new_post = news_post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            if news_post_image_form.is_valid() and request.FILES["image"]:
                new_post_image = news_post_image_form.save(commit=False)
                new_post_image.news_post = new_post
                new_post_image.uploaded_by = request.user
                new_post_image.save()

            messages.info(request, 'News Post Created')
            return redirect("view_news")
        else:
            messages.info(request, message=f'{news_post_form.errors}; {news_post_image_form.errors}')
            news_post_form = NewsPostForm()
            news_post_image_form = NewsPostImageForm()
            return render(request, "main/create_news_post.html", {"news_post_form": news_post_form, "news_post_image_form": news_post_image_form})
    else:
        news_post_form = NewsPostForm()
        news_post_image_form = NewsPostImageForm()
        return render(request, "main/create_news_post.html", {"news_post_form": news_post_form, "news_post_image_form": news_post_image_form})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def upload_multi_gallery_image(request):
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form_gallery = request.POST["gallery"]
            gallery_instance = get_object_or_404(Gallery, pk=int(form_gallery))
            upload_count = 0
            for image_file in request.FILES.getlist("image"):
                new_image = GalleryImage(
                    image=image_file, gallery=gallery_instance, uploaded_by=request.user
                )
                new_image.save()
                upload_count += 1
            messages.info(
                request, message=f"Successfully Uploaded {upload_count} Image(s)"
            )
            return redirect("view_gallery", pk=int(form_gallery))

    else:
        form = GalleryImageForm()
        return render(request, "upload/gallery_image_upload.html", {"form": form})

