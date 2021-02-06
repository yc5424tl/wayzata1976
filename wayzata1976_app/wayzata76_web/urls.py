from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.index, name="index"),
    path("photo/gallery/<int:pk>/", views.view_gallery, name="view_gallery"),
    path("zietgeist/", views.view_zietgeist, name="view_zietgeist"),
    path("classmates/", views.view_classmates, name="view_classmates"),
    path("contact/", views.contact_info, name="contact_info"),
    path("news/view/", views.view_news, name="view_news"),
    path("news/post/", views.create_news_post, name="create_news_post"),
    path("survey/", views.questionnaire, name="questionnaire"),
    path(
        "photo/upload/gallery/", views.upload_gallery_image, name="upload_gallery_image"
    ),
    path(
        "photo/upload/newspost/",
        views.upload_news_post_image,
        name="upload_news_post_image",
    ),
    path(
        "photo/upload/multi/",
        views.upload_multi_gallery_image,
        name="upload_multi_gallery_image",
    ),
    path(
        "password_reset",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            success_url=reverse_lazy("wayzata76_web:password_reset_done"),
        ),
        name="password_reset",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]