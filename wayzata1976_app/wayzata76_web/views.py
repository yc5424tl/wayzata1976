from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import GalleryImage, Person, CustomUser, NewsPostImage, SurveyResult, ContactInfo, NewsPost
from .forms import UploadGalleryImageForm, CustomUserCreationForm, MultiUploadGalleryImageForm, UploadNewsPostImageForm, TestUploadForm, ContactUpdateForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.paginator import Paginator


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
            return render(request, 'main/questionnaire.html')
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


def view_gallery(request):
    pass


def view_zietgeist(request):
    pass


# def view_classmates(request):
#     # classmates = Person.objects.only('is_classmate', 'first_name', 'last_name', 'middle_initial', 'address').filter('is_classmate').order_by('last_name').select_related('address')
#     classmates = Person.objects.filter('is_classmate'== True).only('last_name', 'first_name', 'middle_initial', 'address').order_by('last_name').select_related('address')o


def ClassmateList(ListView):
    template_name = 'main/view_classmates.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = Person.objects.filter('is_classmate' == True).only('last_name', 'first_name', 'middle_initial', 'address', 'is_classmate').order_by('last_name').select_related('address')
        return queryset


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
# class


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