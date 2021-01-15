from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from wayzata76_web.models import GalleryImage
from wayzata76_web.forms import UploadGalleryImageForm,CustomUserCreationForm, MultiUploadGalleryImageForm
from django.http import HttpResponse, JsonResponse


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


def view_gallery(request):
    pass


def view_zietgeist(request):
    pass


def view_classmates(request):
    classmates = Person.objects.only('is_classmate', 'first_name', 'last_name', 'middle_initial', 'address').filter('is_classmate').order_by('last_name').select_related('address')
    return render(template_name='main/view_classmates.html', request=request, context={'classmates': classmates})

def view_links(request):
    pass


def view_contact(request):
    pass


def view_news(request):
    pass


def view_galleries(request):
    pass


def upload_newspost_image(request):
    if request.method == 'POST':
        form = UploadNewsPostImageForm(request.POST, request.FILES, request=request, user=request.user)
        if form.is_valid():
            news_post_image = form.save(commit=False)
            news_post_image.uploaded_by = request.user
            news_post_image.save()


def upload_gallery_image(request):
    if request.method == 'POST':
        form = UploadGalleryImageForm(request.POST, request.FILES, request=request, user=request.user)

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
        form = MultiUploadGalleryImageForm()
        return render(self, 'upload/multi_upload_gallery_image_upload.html')
    elif requewst_method == 'POST':
        form = MultiUploadGalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            data = {'is_valid': True, 'title': image.file.name}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
# class


def success(request):
    return HttpResponse('successfully uploaded')