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
    Отображает главную страницу и делается запрос в БД для получения услуг service
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
    Делается запрос в БД service для отображения услуг в шапке header и profile_all для получения всех
    всех данных пользователя
    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей профиля пользователя и форму для заполнения профиля.
    """
    service = Service.objects.all()
    profile_all = Profile.objects.filter(user=request.user.id)
    if request.method == "POST":
        form = ProfileModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
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
    Делается запрос в БД service для отображения услуг в шапке header и получения instance делается запрос в
    profile_user в БД
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


@login_required(login_url="users:login")
def service_view(request: HttpRequest) -> HttpResponse:
    """
    Отображает все услуги.
    Делается запрос в БД service для отображения услуг
    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей всех услуг
    """
    service = Service.objects.all()
    return render(request, "service.html", context={"service": service})


@login_required(login_url="users:login")
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


@login_required(login_url="users:login")
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


@login_required(login_url="users:login")
def comment_add(request: HttpRequest) -> HttpResponse:
    """
    Отображает форму добавления комментария и подключен celery для фильтрации матов

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


@cache_page(259200)  # кэш на 3 дня
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
    # код блока ниже для чего, добавляется дефиз, потому что в photogallery.html
    # есть data-filter, который не хочет высвечивать определенные фото с пробелом
    # поэтому приходится добавлять везде дефиз
    photo_illu = PhotoGallery.objects.all()
    category_names = set()
    new_photo_illu = []
    for i in photo_illu:
        category_name = i.category.slug
        if category_name not in category_names:
            category_names.add(category_name)
            i.category.slug = category_name
            new_photo_illu.append(i)
    photo_illu = new_photo_illu
    return render(
        request,
        "photogallery.html",
        context={"service": service, "gallery": photo_illu, "gallery_image": photo},
    )


def contact(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу контакты и делается запрос в БД для получения услуг service
    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP страница контакты
    """
    service = Service.objects.all()
    return render(request, "contact.html", context={"service": service})
