from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from website.models import Service

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


class History(Appointment):
    created_at = models.DateField(auto_now_add=True)