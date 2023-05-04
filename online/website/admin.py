from django.contrib import admin
from .models import Service, Profile, CommentWebsite, PhotoGallery
from django.utils.html import format_html
from django.utils.html import mark_safe


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Класс, определяющий настройки административного интерфейса для модели Service.
    """
    list_display = ['name', 'description_service', 'cost_service']
    list_filter = ('name',)

    @staticmethod
    def description_service(obj):
        """
        Функция для форматирования поля description
        """
        return format_html("<b><i>{}</i></b>", f"{obj.description}")

    @staticmethod
    def cost_service(obj):
        """
        Функция для форматирования поля cost
        """
        return format_html("<b><i>{}</i></b>", f"{obj.cost} бел.руб")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Класс, определяющий настройки административного интерфейса для модели Profile.
    """
    list_display = ['user', 'first_name_profile', 'last_name_profile']
    search_fields = ('user__username__startswith',)

    @staticmethod
    def first_name_profile(obj):
        """
        Функция для форматирования поля first_name
        """
        return format_html("<b><i>{}</i></b>", f"{obj.first_name}")

    @staticmethod
    def last_name_profile(obj):
        """
        Функция для форматирования поля last_name
        """
        return format_html("<b><i>{}</i></b>", f"{obj.last_name}")


@admin.register(CommentWebsite)
class CommentWebsiteAdmin(admin.ModelAdmin):
    """
    Класс, определяющий настройки административного интерфейса для модели CommentWebsite.
    """
    list_display = ['user', 'text_comment', 'pub_date_comment', 'update_date_comment']

    @staticmethod
    def text_comment(obj):
        """
        Функция для форматирования поля text
        """
        return format_html("<b><i>{}</i></b>", f"{obj.text}")

    @staticmethod
    def pub_date_comment(obj):
        """
        Функция для форматирования поля pub_date
        """
        return format_html("<b><i>{}</i></b>", f"{obj.pub_date}")

    @staticmethod
    def update_date_comment(obj):
        """
        Функция для форматирования поля update_date
        """
        return format_html("<b><i>{}</i></b>", f"{obj.update_date}")

    search_fields = ('user__username__startswith',)


@admin.register(PhotoGallery)
class PhotoGalleryAdmin(admin.ModelAdmin):
    """
    Класс, определяющий настройки административного интерфейса для модели PhotoGallery.
    """
    list_display = ['id', 'name_category', 'photo_preview']

    @staticmethod
    def name_category(obj):
        """
        Функция для форматирования поля name
        """
        return format_html("<b><i>{}</i></b>", f"{obj.category}")

    @staticmethod
    def photo_preview(obj):
        """
        Функция для отображения поля photo_gallery
        """
        return mark_safe(
            f'<img src = "{obj.photo_gallery.url}" width ="150px" height="200px"/>'
        )
