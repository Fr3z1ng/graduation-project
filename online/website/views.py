from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from booking.models import Appointment, HistoryBooking
from .models import Service, Profile
from .forms import ProfileModelForm
from django.urls import reverse
from .models import Profile
from datetime import datetime
from django.utils import timezone
import pytz


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
    some_list = []
    if appointments_time != some_list:
        for appointment in appointments_time:
            history = HistoryBooking()
            history.user = appointment.user
            history.service = appointment.service
            history.day = appointment.day
            history.time = appointment.time
            history.time_ordered = appointment.time_ordered
            history.save()
        appointments_time.delete()
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
