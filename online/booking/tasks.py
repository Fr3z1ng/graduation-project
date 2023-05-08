import os
from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv

from .models import Appointment, BookingSettings

load_dotenv()


@shared_task
def check_appointments():
    """
    Проверяет у пользователя если есть сегодня посещение,то приходит напоминание на почту

    """
    now = datetime.now()

    appointments = Appointment.objects.filter(day=now.date())

    for appointment in appointments:
        message = f"Пользователь {appointment.user} у вас сегодня посещение мастера {appointment.time}"
        send_mail(
            "Напоминание о посещение",
            message,
            os.environ.get("EMAIL_HOST_USER"),
            [appointment.user.email],
            fail_silently=False,
        )


@shared_task()
def notifacation_record(appoint_id: int):
    """
    Посылает на почту мастеру,что в такой день к нему записались на приём

    Args:
        appoint_id (int): идентификационный номер записи

    """
    appointment = Appointment.objects.get(pk=appoint_id)
    message = (
        f"Пользователь {appointment.user} записался на {appointment.service} "
        f"в такой день {appointment.day} в такое время {appointment.time}"
    )
    send_mail(
        "К вам записались",
        message,
        os.environ.get("EMAIL_HOST_USER"),
        [appointment.user.email],
        fail_silently=False,
    )


@shared_task
def check_time_delete():
    """
    Проверяет если время записи окончилось на сегодняший день,то этот день пропадает из списка дней для записи

    """
    now = datetime.now().date()

    booking_settings = BookingSettings.objects.all()

    for i in booking_settings:
        if i.start_time <= now and i.start_time < i.end_time:
            i.start_time = now + timedelta(days=1)
            i.save()
