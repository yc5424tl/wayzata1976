import json
import os
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .forms import (
    ContactUpdateForm,
    CustomUserCreationForm,
    UploadGalleryImageForm,
    UploadNewsPostImageForm,
    # MultiUploadForm
    NewsPostForm,
    ExtendedNewsPostForm,
    GalleryImageUploadForm
)
from .models import (
    ContactInfo,
    CustomUser,
    Gallery,
    GalleryImage,
    NewsPost,
    NewsPostImage,
    Person,
    SurveyResult,
    Yearbook,
)


def SignUpView(CreateView):
    form_class = CustomUserCreationForm
    succes_url = reverse_lazy("login")
    template_name = "registration.signup.html"


def login(request):
    if request.method == 'GET':
        return render('registration/login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('index')
        else:
            messages.warning(request, "Username/Password Incorrect")
            return redirect('index')


def index(request):
    return render(template_name="main/index.html", request=request)


def questionnaire(request):
    if request.method == "POST":
        liked = request.POST["liked"]
        disliked = request.POST["disliked"]
        location = request.POST["location"]
        music = request.POST["music"]
        music_other = request.POST["music_other"]
        misc = request.POST["misc"]
        submitted_by = request.POST["name"]
        email = request.POST["email"]

        new_result = SurveyResult(
            liked=liked,
            disliked=disliked,
            location=location,
            music=music,
            music_other=music_other,
            misc=misc,
            submitted_by=submitted_by,
            email=email,
        )
        if new_result.has_content:
            new_result.save()
            messages.success(
                request, "Thank you, your questionnaire has been submitted!"
            )
            return render(request, "main/index.html")
        else:
            new_result.delete()
            messages.warning(
                request, "A blank questionnaire cannot be submitted, please try again."
            )
            return render(request, "main/questionnaire.html")
    else:
        return render(request, "main/questionnaire.html")


def contact_info(request):
    if request.method == "POST":
        form = ContactUpdateForm(request.POST)
        if form.is_valid():
            contact_info = form.save(commit=False)
            if request.user.is_authenticated:
                contact_info.user = request.user
            contact_info.save()
            messages.success(
                request, message=
                "Updated contact information has been submitted. Please allow 1-2 days for the  Thank you.",
            )
            # TODO - if submitter is logged in user, check to see if user is attatched to a person -- update corresponding fields
            # TODO - check if all Address fields contain data, create new Address if so, linking it to Person

            # messages.warning(request, message)
    else:
        form = ContactUpdateForm()
        # TODO -- if request.user.is_authenticated --> prefill email/name/address on form
    return render(request, "main/contact_update.html", {"form": form})


def view_gallery(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    return render(request, "main/view_gallery.html", {"gallery": gallery})


def view_zietgeist(request):
    awards = [
        {"award": "Best Picture", "winner": "Rocky"},
        {"award": "Best Actor", "winner": "Peter Finch (Network)"},
        {"award": "Best Actress", "winner": "Faye Dunaway (Network)"},
        {
            "award": "Best Supporting Actor",
            "winner": "Jason Robards (All the President's Men)",
        },
        {"award": "Best Supporting Actress", "winner": "Beatrice Straight (Network)"},
        {"award": "Best Director", "winner": "John Avildsen (Rocky)"},
    ]
    yearbooks = Yearbook.objects.all()
    songs = None
    with open(os.path.join(settings.STATIC_ROOT, "json/songs.json")) as file:
        songs = json.load(file)
    return render(
        request,
        "main/zietgeist.html",
        {"yearbooks": yearbooks, "songs": songs, "awards": awards},
    )


def view_classmates(request):

    classmates = (
        Person.objects.filter(is_classmate=True)
        .only("last_name", "first_name", "middle_initial", "address", "is_classmate")
        .order_by("last_name")
        .select_related("address")
    )

    mia_list = (
        Person.objects.filter(address=None, is_classmate=True)
        .only("last_name", "first_name", "middle_initial", "address", "is_classmate")
        .order_by("last_name")
        .select_related("address")
    )

    passed_list = (
        Person.objects.filter(address__city="passed")
        .only("last_name", "first_name", "middle_initial", "address", "is_classmate")
        .order_by("last_name")
        .select_related("address")
    )

    in_contact_list = (
        Person.objects.exclude(Q(address__city="passed") | Q(address=None))
        .order_by("last_name")
        .select_related("address")
    )

    alphabet = list(string.ascii_uppercase)

    #  Create a dictionary with null values to be replaced by the first student (alphabetically) for each letter, the resulting dictionary contains the Person objects to be targeted with anchor links in the classmates list jump menu.

    all_link_dict = {letter: None for letter in alphabet}
    for letter_key in all_link_dict:
        if letter_key == "X":
            continue
        else:
            for classmate in classmates:
                if classmate.last_name[0] == letter_key:
                    all_link_dict[letter_key] = classmate
                    break

    mia_link_dict = {letter: None for letter in alphabet}
    for letter_key in mia_link_dict:
        if letter_key in ["X", "Q", "U", "X", "Y", "Z"]:
            continue
        else:
            for classmate in mia_list:
                if classmate.last_name[0] == letter_key:
                    mia_link_dict[letter_key] = classmate
                    break

    in_c_link_dict = {letter: None for letter in alphabet}
    for letter_key in in_c_link_dict:
        if letter_key in ["I", "U", "X"]:
            continue
        else:
            for classmate in in_contact_list:
                if classmate.last_name[0] == letter_key:
                    in_c_link_dict[letter_key] = classmate
                    break

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
            "alphabet": alphabet,
        },
    )


class ClassmateList(ListView):
    template_name = "main/view_classmates.html"
    paginate_by = 50
    context_object_name = "classmates"

    def get_queryset(self):
        self.queryset = (
            Person.objects.filter(address=None)
            .only(
                "last_name", "first_name", "middle_initial", "address", "is_classmate"
            )
            .order_by("last_name")
            .select_related("address")
        )
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(ClassmateList, self).get_context_data(**kwargs)
        context["classmates"] = self.queryset
        context["mia_list"] = (
            Person.objects.filter(address=None)
            .only(
                "last_name", "first_name", "middle_initial", "address", "is_classmate"
            )
            .order_by("last_name")
            .select_related("address")
        )
        context["passed_list"] = (
            Person.objects.filter(address__city="passed")
            .only(
                "last_name", "first_name", "middle_initial", "address", "is_classmate"
            )
            .order_by("last_name")
            .select_related("address")
        )
        context["in_contact_list"] = (
            Person.objects.exclude(address__city="passed", address=None)
            .order_by("last_name")
            .select_related("address")
        )
        return context



def view_news(request):
    posts = NewsPost.objects.all()
    return render(request, "main/view_news.html", {"posts": posts})


def upload_news_post_image(request, pk):
    if request.method == "POST":
        form = UploadNewsPostImageForm(request.POST, request.FILES)
        if form.is_valid():
            newspost = NewsPost.objects.get(pk=request.POST.get('newspost_id'))
            print(f'newspost title/id = {newspost.header} @ {newspost.id}')
            news_post_image = form.save(commit=False)
            news_post_image.uploaded_by = request.user
            news_post_image.news_post = newspost
            news_post_image.save()
            return redirect("view_news")
        else:
            print('newsimageform is not valid')
            print(f'form.errors = {form.errors}')
            form = UploadNewsPostImageForm()
            return render(request, 'upload/upload_news_post_image.html', {'form': form, 'pk': pk})
    else:
        newspost = get_object_or_404(NewsPost, pk=pk)
        print(f'newspost header/id = {newspost.header} @ {newspost.id}')
        form = UploadNewsPostImageForm()
        # user = CustomUser(pk=request.user.pk)
        # uploaded_news_post_images = request.user.news_post_images.all()
        # uploaded_gallery_images = request.user.gallery_images.all()
        return render(
            request,
            "upload/upload_news_post_image.html",
            {
                "form": form,
                # "news_post_images": uploaded_news_post_images,
                # "gallery_images": uploaded_gallery_images,
                'newspost_pk': pk
            }
        )


def upload_gallery_image(request):

    if request.method == "POST":
        form = UploadGalleryImageForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            gallery_image = form.save(commit=False)
            gallery_image.uploaded_by = request.user
            gallery_image.save()
            return redirect("index")
    else:
        form = UploadGalleryImageForm()
    return render(request, "upload/local_image_upload.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_news_post(request):
    if request.method == 'POST':
        form = ExtendedNewsPostForm(request.POST)
        if form.is_valid():
            print('news post form is valid')
            # print(f'form.cleaned_data.get(header) = {form.cleaned_data.get("header")}')
            # print(f'form.cleaned_data.get(body) = {form.cleaned_data.get("body")}')
            new_post = form.save(commit=False)
            new_post.author = request.user
            # new_post.header = form.cleaned_data.get('header')
            # new_post.body = form.cleaned_data.get('body')
            new_post.save()

            new_post = NewsPost(
                header=form.cleaned_data.get('header'),
                body=form.cleaned_data.get('body'),
                author=request.user,
                link=form.cleaned_data.get('link'),
                link_text = form.cleaned_data.get('link_text')
            )

            new_post.save()
            print('saved new_post')
            # if form.cleaned_data.get('image'):
            #     print('inside form.cleaned_data.get(image)')
            #     post_image = NewsPostImage(
            #         news_post=new_post,
            #         image=form.cleaned_data.get('image'),
            #         uploaded_by=request.user,
            #         title=form.cleaned_data.get('subtitle')
            #     )
            #     post_image.save()
            # else:
            #     print('image from form is not clean')
            if request.FILES['image']:
                print('inside if request.FILES["image"]')
                post_image = NewsPostImage(
                    image=request.FILES['image'],
                    subtitle=form.cleaned_data['subtitle'],
                    uploaded_by=request.user,
                    news_post=new_post
                )
                post_image.save()
                print('saved post_image')

            # upload_news_image_form = UploadNewsPostImageForm()
            print('returning from news post form is valid')
            return redirect('view_news')
            # return render(request, 'upload/upload_news_post_image.html', {'pk': new_post.pk, 'form': upload_news_image_form})
        else:
            print('news_post_form is invalid')
            print(form.errors)
            # new_post = NewsPost(
            #     author=request.user,
            #     header=form.cleaned_data.get('header'),
            #     body=form.cleaned_data.get('body'),
            #     link=form.cleaned_data.get('link'),
            #     link_text=form.cleaned_data.get('link-text')
            # )
            # new_post.save()
            # messages.info(request, f"{', '.join([form.errors[error] for error in form.errors])}")
            messages.info(request, form.errors)
            form = ExtendedNewsPostForm()
            print('returning from newspostform has errors')
            return render(request, 'main/create_news_post.html', {'form': form})
    else:
        form = ExtendedNewsPostForm()
        print('returning from createnewspost GET requiest')
        return render(request, 'main/create_news_post.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def upload_multi_gallery_image(request):
    if request.method == 'POST':
        form = GalleryImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form_gallery = request.POST['gallery']
            gallery_instance = get_object_or_404(Gallery, pk=int(form_gallery))
            upload_count = 0
            for image_file in request.FILES.getlist('image'):
                new_image = GalleryImage(
                    image = image_file,
                    gallery = gallery_instance,
                    uploaded_by=request.user
                )
                new_image.save()
                upload_count += 1
            messages.info(request, message=f'Successfully Uploaded {upload_count} Image(s)')
            return redirect('view_gallery', pk=int(form_gallery))

            # print(f'form value from request.POST = {request.POST["gallery"]}')
            # print(f'request.FILES = {request.FILES['image']}')
            # gallery_image = form.save(commit=False)
            # gallery_image.uploaded_by = request.user
            # gallery_image.gallery = gallery_instance
            # gallery_image.save()
            # messages.info(request, message='Image Upload Success')
            # return redirect('index')
        # print(f'type(request.POST) = {type(request.POST)}')
        # print(f'request.POST = {request.POST}')
        # print(f'request.FILES = {request.FILES}')
        # print(f'request.POST["gallery"] = {request.POST["gallery"]}')
        # target_gallery = get_object_or_404(Gallery, pk=int(request.POST['gallery']))
        # target_gallery = request.POST['gallery']
        # upload_count = 0
        # for image_file in request.POST['image']:
            # print(f'type(image_file) = {type(image_file)}')
            # print(f'image_file = {image_file}')
            # new_image = GalleryImage(
                # image=image_file,
                # gallery=target_gallery,
                # uploaded_by=request.user
            # )
            # new_image.save()
            # upload_count += 1
            # messages.info(request, message=f'Successfully Uploaded {upload_count} images')
        # return redirect('view_gallery', pk=target_gallery.pk)

        # return redirect(reverse('view_classmates'))
    else:
        form = GalleryImageUploadForm()
        return render(request, 'upload/gallery_image_upload.html', {'form': form})
    
# request.POST = <QueryDict: {
    # 'csrfmiddlewaretoken': ['a03Z1HdQ3RE69YSO70Xae1eMkyxFb3BVYcM6WtlvclYkKY5GXjLfu46g93eKYGhI'], 
    # 'image': ['---_0056.jpg', '---_0059.jpg'], 
    # 'gallery': ['9']}>
# request.FILES = <MultiValueDict: {}>
# request.POST["gallery"] = 9

# def multi_upload_gallery(request, gallery_pk):
    # gallery = get_object_or_404(Gallery, pk=gallery_pk)

# def multi_upload(request):
#     if request.method == 'GET':
#         form = MultiUploadForm
#         return render(request, 'upload/multi_upload.html', {"form": form})


# @ensure_csrf_cookie
# def upload_file(request):
#     if request.method == 'POST':
#         form = MultiUploadForm(request.POST, request.FILES)
#         files = request.FILES.getlist('files')
#         if form.is_valid():
#             for f in files:
#                 handle_uploaded_file(f)
#             handle_uploaded_file(request.FILES['image'])
#             messages.info(request, 'Files Successfully Uploaded')
#             context = {'msg': '<span style="color: green;">File successfully uploaded</span>'}
#             # return render(request, "upload/multi_upload.html", context)
#             return redirect('index', message="successfull upload")
#         else:
#             messages.error(request, 'Error uploading files')
#             return redirect('index')
#     else:
#         form = MultiUploadForm()
#         return render(request, 'upload/multi_upload.html', {'form': form})

# def handle_uploaded_file(f):
#     with open(f.name, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)