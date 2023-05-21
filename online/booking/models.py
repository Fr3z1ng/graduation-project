from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from website.models import Service

from .constant import TIMES

TIME_CHOICES = [(x, x) for x in TIMES]


class Appointment(models.Model):
    """
    Модель записи времени
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True
    )
    day = models.DateField(default=datetime.now)
    time = models.CharField(max_length=40, choices=TIME_CHOICES, default="12.00")
    time_ordered = models.DateTimeField(default=datetime.now, blank=True)


class HistoryBooking(models.Model):
    """
    Модель истории записи
    """

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
    """
    Модель выбора времени работ мастера
    """

    start_time = models.DateField(default=datetime.now)
    end_time = models.DateField()

    def clean(self):
        """
        Валидация на правильный выбор данных
        """

        if self.start_time >= self.end_time:
            raise ValidationError("Start_time не должен быть равен или больше End_time")
