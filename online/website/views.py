from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic.edit import DeleteView, UpdateView

from .forms import CommentModelForm, ProfileEditModelForm, ProfileModelForm
from .models import CommentWebsite, PhotoGallery, Profile, Service
from .tasks import replace_text_with_censored


def index(request: HttpRequest) -> HttpResponse:
    """
    Отображает главную страницу

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP с главной страницей
    """
    service = Service.objects.all()
    return render(request, "main.html", context={"service": service})


@login_required(login_url="users:login")
def profile(request: HttpRequest) -> HttpResponse:
    """
    Отображает профиль пользователя и форму для заполнения профиля если это требуется.

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей профиля пользователя и форму для заполнения профиля.
    """
    service = Service.objects.all()
    profile_all = Profile.objects.filter(user=request.user.id)
    prof = Profile()
    if request.method == "POST":
        form = ProfileModelForm(request.POST, request.FILES)
        if form.is_valid():
            prof.first_name = form.cleaned_data["first_name"]
            prof.last_name = form.cleaned_data["last_name"]
            prof.phone_number = form.cleaned_data["phone_number"]
            prof.profile_image = form.cleaned_data["profile_image"]
            prof.user = request.user
            prof.save()
            return redirect(reverse("website:profile"))
    else:
        form = ProfileModelForm()
    return render(
        request,
        "profile.html",
        context={"profile": profile_all, "form": form, "service": service},
    )


@login_required(login_url="users:login")
def profile_edit(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу с формой для изменения профиля.

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей профиля пользователя
    """
    service = Service.objects.all()
    profile_user = Profile.objects.get(user=request.user.id)
    if request.method == "POST":
        form = ProfileEditModelForm(
            request.POST, request.FILES, instance=profile_user
        )  # передать текущий профиль в качестве экземпляра instance
        if form.is_valid():
            form.save()  # сохранить изменения
            return redirect(reverse("website:profile"))
    else:
        form = ProfileEditModelForm(instance=profile_user)
    return render(
        request,
        "profile_edit.html",
        context={"profile": profile_user, "form": form, "service": service},
    )


def service_view(request: HttpRequest) -> HttpResponse:
    """
    Отображает все услуги.

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей всех услуг
    """
    service = Service.objects.all()
    return render(request, "service.html", context={"service": service})


def service_info(request, pk: int) -> HttpResponse:
    """
    Отображает информацию об услуге.

    Args:
        request (HttpRequest): объект запроса HTTP
        pk(int): Идентификатор услуги
    Returns:
        HttpResponse: объект ответа HTTP со страницей информации об услуге
        :param request:
        :param pk:
    """
    service = Service.objects.all()
    service_information = Service.objects.get(pk=pk)
    return render(
        request,
        "service_info.html",
        context={"service": service, "service_info": service_information},
    )


def comments(request: HttpRequest) -> HttpResponse:
    """
    Отображает все комментарии.

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей всех комментариев
    """
    service = Service.objects.all()
    comment_user = CommentWebsite.objects.filter(user=request.user)
    comment_another_users = CommentWebsite.objects.exclude(user=request.user)
    return render(
        request,
        "website/comment.html",
        context={
            "comment_user": comment_user,
            "comment_another_users": comment_another_users,
            "service": service,
        },
    )


def comment_add(request: HttpRequest) -> HttpResponse:
    """
    Отображает форму добавления комментария

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей формы добавления комментария
    """
    if request.method == "POST":
        comment_form = CommentModelForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            if request.user.is_authenticated:
                new_comment.user = request.user
            else:
                new_comment.user = None
                return redirect(reverse("users:login"))
            new_comment.save()
            replace_text_with_censored.delay(new_comment.id)
            return redirect(reverse("website:comment"))
    else:
        comment_form = CommentModelForm()
    return render(request, "website/comment_form.html", context={"form": comment_form})


class CommentUpdateView(UpdateView):
    """Представление для редактирования существующего комментария."""

    model = CommentWebsite
    form_class = CommentModelForm
    context_object_name = "comment"
    template_name_suffix = "_update"


class CommentDeleteView(DeleteView):
    """Представление для удаления существующего комментария."""

    model = CommentWebsite
    success_url = reverse_lazy("website:comment")
    context_object_name = "comment"
    template_name_suffix = "_delete"


def gallery(request: HttpRequest) -> HttpResponse:
    """
    Отображает фотогалерею

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей отображения фотогалереи
    """
    service = Service.objects.all()
    photo = PhotoGallery.objects.all()
    for i in photo:
        i.category.name = i.category.name.replace(" ", "-")
    photo_illu = PhotoGallery.objects.all()
    category_names = set()
    new_photo_illu = []
    for i in photo_illu:
        category_name = i.category.name.replace(" ", "-")
        if category_name not in category_names:
            category_names.add(category_name)
            i.category.name = category_name
            new_photo_illu.append(i)
    photo_illu = new_photo_illu
    return render(
        request,
        "Photogallery.html",
        context={"gallery": photo, "service": service, "gallery_illu": photo_illu},
    )
