from django.contrib import admin
from .models import Service, Profile, CommentWebsite, PhotoGallery


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "cost"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]


@admin.register(CommentWebsite)
class CommentWebsiteAdmin(admin.ModelAdmin):
    list_display = ["user", "text", 'pub_date', 'update_date']


@admin.register(PhotoGallery)
class PhotoGalleryAdmin(admin.ModelAdmin):
    list_display = ['photo_gallery', 'short_description']
