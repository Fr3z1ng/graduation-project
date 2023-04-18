from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from booking.models import Appointment, HistoryBooking
from .models import Service, Profile, CommentWebsite, PhotoGallery
from .forms import ProfileModelForm, CommentModelForm
from django.urls import reverse, reverse_lazy
from .models import Profile
from datetime import datetime
from django.core import serializers
from .tasks import replace_text_with_censored


def index(request: HttpRequest):
    """
    Представление для всех категорий
    """
    return render(request, "main.html")


@login_required(login_url="users:login")
def profile(request):
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
    some_list = []
    appointments = Appointment.objects.filter(user=request.user)
    appointments_day = Appointment.objects.filter(day__lt=now.date())
    appointments_time = Appointment.objects.filter(day=now.date(), time__lt=now.time())
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
    if appointments_day != some_list:
        for appointment in appointments_day:
            history = HistoryBooking()
            history.user = appointment.user
            history.service = appointment.service
            history.day = appointment.day
            history.time = appointment.time
            history.time_ordered = appointment.time_ordered
            history.save()
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


def comments(request):
    """
    Представление для конкретной услуги
    """
    comment_user = CommentWebsite.objects.filter(user=request.user)
    comment_another_users = CommentWebsite.objects.exclude(user=request.user)
    if request.method == 'POST':
        comment_form = CommentModelForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.save()
            replace_text_with_censored.delay(new_comment.id)
    else:
        comment_form = CommentModelForm()
    return render(request, "website/comment.html",
                  context={'comment_user': comment_user, 'comment_another_users': comment_another_users,
                           'form': comment_form})


class CommentCreateView(CreateView):
    model = CommentWebsite
    form_class = CommentModelForm


class CommentUpdateView(UpdateView):
    model = CommentWebsite
    form_class = CommentModelForm  # добавил валидацию для редактирования комментария
    context_object_name = 'comment'
    template_name_suffix = '_update'


class CommentDeleteView(DeleteView):
    model = CommentWebsite
    success_url = reverse_lazy(
        "website:comment"
    )
    context_object_name = 'comment'
    template_name_suffix = '_delete'


def gallery(request):
    """
    Представление для конкретной услуги
    """
    photo = PhotoGallery.objects.all()
    return render(request, "Photogallery.html", context={'photo': photo})
