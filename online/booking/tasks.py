import os

from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime
from .models import Appointment
from dotenv import load_dotenv

load_dotenv()


@shared_task
def check_appointments():
    # Получаем текущую дату и время
    now = datetime.now()

    # Извлекаем все записи на визиты, у которых дата записи равна текущей дате
    appointments = Appointment.objects.filter(day=now.date())
    # Проверяем каждую запись на предстоящий визит
    for appointment in appointments:
        message = f'Пользователь {appointment.user} у вас сегодня посещение мастера {appointment.time}'
        # Вызываем функцию для отправки уведомления о визите
        send_mail('Напоминание о посещение', message, os.environ.get('EMAIL_HOST_USER'), [appointment.user.email],
                  fail_silently=False)
