from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from .models import Service


def index(request: HttpRequest):
    """
    Представление для всех категорий
    """
    return render(request, "main.html")


def profile(request: HttpRequest):
    """
    Представление для всех категорий
    """
    send_mail(
        'Subject here',
        'Here is the message.',
        'beste1997@mail.ru',
        ['alex_bestee@mail.ru'],
        fail_silently=False,
    )
    return render(request, "profile.html")


def service_view(request: HttpRequest):
    """
    Представление для всех категорий
    """
    service = Service.objects.all()
    return render(request, "service.html", context={'service': service})


def service_info(request, pk):
    """
    Представление для конкретной услуги
    """
    service = Service.objects.get(pk=pk)
    return render(request, "service_info.html", context={'service': service})
