from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upcoming/', views.upcoming, name='view_upcoming'),
    path('photo/gallery/<int:pk>/', views.view_gallery, name='view_gallery'),
    path('photo/gallery/', views.view_galleries, name='view_galleries'),
    path('zietgeist/', views.view_zietgeist, name='view_zietgeist'),
    path('classmates/', views.view_classmates, name='view_classmates'),
    path('links/', views.view_links, name='view_links'),
    path('contact/', views.contact_info, name='contact_info'),
    path('news/create/', views.create_news_post, name='create_news_post'),
    path('news/', views.view_news, name='view_news'),
    path('survey/', views.questionnaire, name='view_questionnaire'),
    # path('photo/upload/gallery/multi/', views.multi_upload_gallery_image, name='multi_upload_gallery_image'),
    path('photo/upload/gallery/multi/', views.multi_upload_test, name='multi_upload_test'),
    path('photo/upload/gallery/', views.upload_gallery_image, name='upload_gallery_image'),
    path('photo/upload/newspost/', views.upload_news_post_image, name='upload_news_post_image'),
    path('success', views.success, name='success'),

    path('password_reset', auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        success_url=reverse_lazy('wayzata76_web:password_reset_done'),
        ),
        name="password_reset"
    ),

    path('upload_form/', views.test_view, name='test_upload_form'),
    path('test/classmates', views.test_classmates, name="test_classmates"),
]