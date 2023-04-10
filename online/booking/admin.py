from django.contrib import admin
from .models import Appointment, HistoryBooking


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Appointment, AppointmentAdmin)


class HistoryBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'service']


admin.site.register(HistoryBooking, HistoryBookingAdmin)
