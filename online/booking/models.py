from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from website.models import Service
from django.core.exceptions import ValidationError

TIME_CHOICES = (
    ("10.00 PM", "10.00 PM"),
    ("10:30 PM", "10:30 PM"),
    ("11.00 PM", "11.00 PM"),
    ("11:30 PM", "11:30 PM"),
    ("12.00 PM", "12.00 PM"),
    ("12:30 PM", "12:30 PM"),
    ("13.00 PM", "13.00 PM"),
    ("13:30 PM", "13:30 PM"),
    ("14.00 PM", "14.00 PM"),
    ("14:30 PM", "14:30 PM"),
    ("15.00 PM", "15.00 PM"),
    ("15:30 PM", "15:30 PM"),
    ("16.00 PM", "16.00 PM"),
    ("16:30 PM", "16:30 PM"),
    ("17.00 PM", "17.00 PM"),
    ("17:30 PM", "17:30 PM"),
    ("18.00 PM", "18.00 PM"),
)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=10, choices=TIME_CHOICES, default="3 PM")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.user} | day: {self.day} | time: {self.time} | {self.service}"


class HistoryBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
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
            raise ValidationError('Start time should be earlier than end time')
