from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    CustomUser,
    Gallery,
    Image,
    GalleryImage,
    NewsPostImage,
    NewsPost,
    Person,
    SurveyResult,
    Address,
    ContactInfo,
    Yearbook,
)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
    ]


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street",
        "city",
        "state_province",
        "zip_code",
        "country",
        "latitude",
        "longitude",
    )
    list_editable = (
        "street",
        "city",
        "state_province",
        "zip_code",
        "country",
        "latitude",
        "longitude",
    )
    list_filter = (
        "city",
        "state_province",
        "zip_code",
        "country",
        "latitude",
        "longitude",
    )
    list_display_links = None


class GalleryImageAdmin(admin.StackedInline):
    model = GalleryImage


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    inlines = [GalleryImageAdmin]

    list_display = (
        "working_name",
        "display_name",
        "date_created",
        "date_last_modified",
        "section",
        "abstract_gallery",
        "subgallery",
        "parent_gallery",
    )
    list_editable = (
        "working_name",
        "display_name",
        "section",
    )
    list_filter = ("date_created", "date_last_modified", "section", "parent_gallery")
    list_display_links = None


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["gallery", "uuid", "date_created", "title", "subtitle", "uploaded_by", "image", 'thumbnail_preview']
    list_editable = ("gallery", "title", "subtitle")
    list_filter = ("gallery", "date_created", "title", "uploaded_by")
    list_display_links = ("uploaded_by",)
    readonly_fields = ('thumbnail_preview', )

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail'
    # thumbnail_preview.allow_tags = True

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("header", "body", "author", "date_created")
    list_editable = ("header", "body")
    list_filter = ("author", "date_created")
    list_display_links = ("author",)


@admin.register(NewsPostImage)
class NewsPostImageAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "date_created",
        "title",
        "subtitle",
        "uploaded_by",
        "news_post",
    )
    list_editable = ("title", "subtitle")
    list_filter = ("date_created", "news_post", "uploaded_by")
    list_display_links = ("uploaded_by", "news_post")


def news_post_image_path(instance, filename):
    name, ext = filename.split(".")
    file_path = f"news_post_image/{instance.uuid}.{ext}"
    return file_path


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "last_name",
        "first_name",
        "middle_initial",
        "nickname",
        "phone",
        "email",
        "is_classmate",
        "is_alumni",
        "is_relative",
        "is_faculty",
        "user",
    )
    list_editable = (
        "address",
        "last_name",
        "first_name",
        "middle_initial",
        "nickname",
        "phone",
        "email",
        "is_classmate",
        "is_alumni",
        "is_relative",
        "is_faculty",
    )
    list_filter = (
        "address",
        "last_name",
        "first_name",
        "middle_initial",
        "nickname",
        "phone",
        "email",
        "is_classmate",
        "is_alumni",
        "is_relative",
        "is_faculty",
    )
    list_display_links = ("user",)


@admin.register(SurveyResult)
class SurveyResultAdmin(admin.ModelAdmin):
    list_display = (
        "liked",
        "disliked",
        "location",
        "music",
        "music_other",
        "misc",
        "submitted_by",
        "email",
        "date_created",
    )
    list_editable = (
        "liked",
        "disliked",
        "location",
        "music",
        "music_other",
        "misc",
        "email",
    )
    list_filter = ("email", "submitted_by", "date_created")
    list_display_links = None


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "middle_initial",
        "last_name",
        "street_address",
        "city",
        "state_province",
        "country",
        "phone",
        "email",
        "spouse_is_classmate",
        "spouse_is_alumni",
        "spouse_first_name",
        "spouse_middle_initial",
        "spouse_last_name",
        "user",
    )
    list_editable = (
        "first_name",
        "middle_initial",
        "last_name",
        "street_address",
        "city",
        "state_province",
        "country",
        "phone",
        "email",
        "spouse_is_classmate",
        "spouse_is_alumni",
        "spouse_first_name",
        "spouse_middle_initial",
        "spouse_last_name",
        "user",
    )
    list_display_links = None


@admin.register(Yearbook)
class YearbookAdmin(admin.ModelAdmin):
    list_display = ("school", "year", "cover", "gallery", "created_by", "date_created")
    list_editable = ("school", "year", "cover")
    list_display_links = ("created_by", "gallery")
