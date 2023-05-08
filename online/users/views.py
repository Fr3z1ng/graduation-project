import os

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetView)
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from dotenv import load_dotenv

from .forms import CustomPasswordChangeForm, CustomUserCreationForm, LoginForm
from .tasks import register_message
from .token import account_activation_token

load_dotenv()


def register(request: HttpRequest) -> HttpResponse:
    """
    Отображает форму регистрации пользователя

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP с формой на странице
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            message = render_to_string(
                "activate_email.html",
                {
                    "user": user,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            register_message.delay(message, to_email)
            return render(request, "users/confirm_email.html")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """
    Активация токена регистрации

    Args:
        request (HttpRequest): объект запроса HTTP
        uidb64 (str): это строка, содержащая 64-битное представление значения целого числа.
        token (str): уникальный токен аутентификации

    Returns:
        HttpResponse: объект ответа HTTP со страницей профиля пользователя и форму для заполнения профиля.
    """

    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse("website:profile"))
    else:
        return render(request, "users/false_email_token.html")


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Отображает форму входа в аккаунт

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP с формой логина на странице
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("website:index"))
                else:
                    return render(request, "users/disabled_acc.html")
            else:
                return render(request, "users/invalid_login.html")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Выход из аккаунта
    """
    logout(request)
    return redirect("website:index")


def password_change(request: HttpRequest) -> HttpResponse:
    """
    Отображает форму изменения пароля

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP с формой отображения изменения пароля
    """
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, "users/password_change_success.html")
    else:
        current_user = request.user
        form = CustomPasswordChangeForm(current_user)
    return render(request, "users/password_change.html", {"form": form})


class MyPasswordResetView(PasswordResetView):
    """Класс для сброса пароля пользователя."""

    email_template_name = "users/password_reset_email.html"
    html_email_template_name = "users/password_reset_email.html"
    from_email = os.environ.get("EMAIL_HOST_USER")
    success_url = reverse_lazy("users:password_reset_done")

    def form_valid(self, form):
        """
        Проверяет, существует ли email-адрес в базе данных и отправляет письмо с инструкцией по сбросу пароля.
        """
        email = form.cleaned_data.get("email")
        user = User.objects.filter(
            email=email
        ).first()  # Используем filter и first вместо get с аргументом default=None
        if not user:
            return render(self.request, "users/reset_email_false.html")
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    """Класс для подтверждения сброса пароля пользователя."""

    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


def password_reset_done(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу с подтвеждением отправки сообщения на почту

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP с формой отображения изменения пароля
    """
    context = {
        "message": "Сброс пароля успешно выполнен! Проверьте почту на наличие письма подтверждение изменения пароля",
    }
    return render(request, "users/password_reset_done.html", context)


def password_reset_complete(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу с подтвеждением изменения пароля

    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP с формой отображения изменения пароля
    """
    context = {
        "message": "Ваш пароль изменен",  # Сообщение, которое вы хотите отобразить на странице
    }
    return render(request, "users/password_reset_complete.html", context)
