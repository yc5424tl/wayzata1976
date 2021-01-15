from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from wayzata76_web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upcoming/', views.upcoming, name='view_upcoming'),
    path('photo/gallery/<int:gallery_pk>/', views.view_gallery, name='view_gallery'),
    path('photo/gallery/', views.view_galleries, name='view_galleries'),
    path('zietgeist/', views.view_zietgeist, name='view_zietgeist'),
    path('classmates/', views.view_classmates, name='view_classmates'),
    path('links/', views.view_links, name='view_links'),
    path('contact/', views.view_contact, name='view_contact'),
    path('news/', views.view_news, name='view_news'),
    path('photo/upload/gallery/multi/', views.multi_upload_gallery_image, name='multi_upload_gallery_image'),
    path('photo/upload/gallery/', views.upload_gallery_image, name='upload_gallery_image'),
    path('photo/upload/newspost/', views.upload_newspost_image, name='upload_newspost_image'),
    path('success', views.success, name='success'),

    path('password_reset', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        success_url=reverse_lazy('wayzata76_web:password_reset_done'),
        ),
        name="password_reset"
    ),
]