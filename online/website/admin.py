from django.contrib import admin
from .models import Service, Profile


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "cost"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name"]
