from django.contrib import admin
from .models import Appointment, History


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Appointment, AppointmentAdmin)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'service']


admin.site.register(History, HistoryAdmin)
