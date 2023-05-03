from django.contrib import admin
from .models import Appointment, HistoryBooking, BookingSettings
from django.utils.html import format_html


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'appointment_service', 'appointment_day', 'appointment_time']
    list_filter = ('day',)
    search_fields = ('user__username__startswith', 'service__name__startswith', 'day__exact',)

    @staticmethod
    def appointment_service(obj):
        return format_html("<b><i>{}</i></b>", f"{obj.service}")

    @staticmethod
    def appointment_day(obj):
        return format_html("<b><i>{}</i></b>", f"{obj.day}")

    @staticmethod
    def appointment_time(obj):
        return format_html("<b><i>{}</i></b>", f"{obj.time}")


@admin.register(BookingSettings)
class BookingSettingsAdmin(admin.ModelAdmin):
    list_display = ['start_time_booking', 'end_time_booking']

    @staticmethod
    def start_time_booking(obj):
        return format_html("<b><i>{}</i></b>", f"{obj.start_time}")

    @staticmethod
    def end_time_booking(obj):
        return format_html("<b><i>{}</i></b>", f"{obj.end_time}")


@admin.register(HistoryBooking)
class HistoryBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'history_service', 'history_day', 'history_time']
    list_filter = ('day',)
    search_fields = ('user__username__startswith', 'service__name__startswith', 'day__exact',)

    @staticmethod
    def history_service(obj):
        return format_html("<b><i>{}</i></b>", f"{obj.service}")

    @staticmethod
    def history_day(obj):
        return format_html("<b><i>{}</i></b>", f"{obj.day}")

    @staticmethod
    def history_time(obj):
        return format_html("<b><i>{}</i></b>", f"{obj.time}")
