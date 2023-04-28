from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from booking.models import Appointment, HistoryBooking
from .models import Service, Profile, CommentWebsite, PhotoGallery
from .forms import ProfileModelForm, CommentModelForm, ProfileEditModelForm
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
            return redirect(reverse('website:profile'))
    else:
        form = ProfileModelForm()
    return render(request, "profile.html",
                  context={'profile': profile_all, 'form': form, 'service': service})


@login_required(login_url="users:login")
def profile_edit(request):
    service = Service.objects.all()
    profile = Profile.objects.get(user=request.user.id)
    if request.method == 'POST':
        form = ProfileEditModelForm(request.POST, request.FILES, instance=profile)  # передать текущий профиль в качестве экземпляра instance
        if form.is_valid():
            form.save()  # сохранить изменения
            return redirect(reverse('website:profile'))
    else:
        form = ProfileEditModelForm(instance=profile)
    return render(request, "profile_edit.html",
                  context={'profile': profile, 'form': form, 'service': service})


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
    service = Service.objects.all()
    service_information = Service.objects.get(pk=pk)
    return render(request, "service_info.html", context={'service': service, 'service_info': service_information})


def comments(request):
    """
    Представление для конкретной услуги
    """
    service = Service.objects.all()
    comment_user = CommentWebsite.objects.filter(user=request.user)
    comment_another_users = CommentWebsite.objects.exclude(user=request.user)
    return render(request, "website/comment.html",
                  context={'comment_user': comment_user, 'comment_another_users': comment_another_users,
                           'service': service})


def comment_add(request):
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
            return redirect(reverse('website:comment'))
    else:
        comment_form = CommentModelForm()
    return render(request, "website/comment_form.html", context={'form': comment_form})


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
    for i in photo:
        i.category.name = i.category.name.replace(' ', '-')
    photo_illu = PhotoGallery.objects.all()
    category_names = set()
    new_photo_illu = []
    for i in photo_illu:
        category_name = i.category.name.replace(' ', '-')
        if category_name not in category_names:
            category_names.add(category_name)
            i.category.name = category_name
            new_photo_illu.append(i)
    photo_illu = new_photo_illu
    return render(request, "Photogallery.html",
                  context={'gallery': photo, 'service': service, 'gallery_illu': photo_illu})
