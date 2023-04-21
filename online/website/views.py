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
from django.db.models import Q


def index(request: HttpRequest):
    """
    Представление для всех категорий
    """
    service = Service.objects.all()
    return render(request, "base.html", context={'service': service})


@login_required(login_url="users:login")
def profile(request):
    service = Service.objects.all()
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
    appointments_expired = Appointment.objects.filter(Q(day__lt=now.date()) | Q(day=now.date(), time__lt=now.time()))

    if appointments_expired:
        for appointment in appointments_expired:
            history = HistoryBooking(user=appointment.user, service=appointment.service, day=appointment.day,
                                     time=appointment.time, time_ordered=appointment.time_ordered)
            history.save()
        appointments_expired.delete()
    return render(request, "profile.html",
                  context={'profile': profile_all, 'form': form, 'appointments': appointments, 'service': service})


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
    service = Service.objects.all()
    comment_user = CommentWebsite.objects.filter(user=request.user)
    comment_another_users = CommentWebsite.objects.exclude(user=request.user)
    if request.method == 'POST':
        comment_form = CommentModelForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            if request.user.is_authenticated:
                new_comment.user = request.user
            else:
                new_comment.user = None
                return redirect(reverse('users:login'))
            new_comment.save()
            replace_text_with_censored.delay(new_comment.id)
    else:
        comment_form = CommentModelForm()
    return render(request, "website/comment.html",
                  context={'comment_user': comment_user, 'comment_another_users': comment_another_users,
                           'service': service,
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
    service = Service.objects.all()
    photo = PhotoGallery.objects.all()
    return render(request, "Photogallery.html", context={'photo': photo, 'service': service})
