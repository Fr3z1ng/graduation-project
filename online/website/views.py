from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from booking.models import Appointment
from .models import Service, Profile
from .forms import ProfileModelForm
from django.urls import reverse
from .models import Profile
from datetime import datetime


def index(request: HttpRequest):
    """
    Представление для всех категорий
    """
    return render(request, "main.html")


def profile(request: HttpRequest):
    """
    Представление для всех категорий
    """
    profile_all = Profile.objects.filter(user=request.user.id)
    prof = Profile()
    if request.method == 'POST':
        form = ProfileModelForm(request.POST, request.FILES)
        if form.is_valid():
            prof.first_name = form.cleaned_data['first_name']
            prof.last_name = form.cleaned_data['last_name']
            prof.phone_number = form.cleaned_data['phone_number']
            prof.profile_image = form.cleaned_data['profile_image']
            prof.user = request.user
            prof.save()
            return render(request, 'profile.html')
    else:
        form = ProfileModelForm()
    now = datetime.now()
    appointments = Appointment.objects.filter(user=request.user)
    appointments_time = Appointment.objects.filter(day=now.date(), time__lt=now.time())
    appointments_day = Appointment.objects.filter(day__lt=now.date(), time__lt=now.time())
    some_list = []
    if appointments_time or appointments_day != some_list:
        appointments_time.delete()
        appointments_day.delete()
    return render(request, "profile.html", context={'profile': profile_all, 'form': form, 'appointments': appointments})


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
