from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from website.models import Service

TIME_CHOICES = (
    ("10.00", "10.00"),
    ("10:30", "10:30"),
    ("11.00", "11.00"),
    ("11:30", "11:30"),
    ("12.00", "12.00"),
    ("12:30", "12:30"),
    ("13.00", "13.00"),
    ("13:30", "13:30"),
    ("14.00", "14.00"),
    ("14:30", "14:30"),
    ("15.00", "15.00"),
    ("15:30", "15:30"),
    ("16.00", "16.00"),
    ("16:30", "16:30"),
    ("17.00", "17.00"),
    ("17:30", "17:30"),
    ("18.00", "18.00"),
)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True
    )
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=40, choices=TIME_CHOICES, default="12.00")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)


class HistoryBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True
    )
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} | day: {self.day} | time: {self.time} | {self.service}"


class BookingSettings(models.Model):
    start_time = models.DateField(default=datetime.now)
    end_time = models.DateField()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time should be earlier than end time")
