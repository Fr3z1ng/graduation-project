from django.contrib import admin
from .models import Appointment, HistoryBooking, BookingSettings


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Appointment, AppointmentAdmin)


class BookingSettingsAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time']


admin.site.register(BookingSettings, BookingSettingsAdmin)


class HistoryBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'service']


admin.site.register(HistoryBooking, HistoryBookingAdmin)
