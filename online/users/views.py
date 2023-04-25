import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from .forms import CustomUserCreationForm, LoginForm, CustomPasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from dotenv import load_dotenv
from .tasks import register_message

load_dotenv()


def register(request):
    """
    Представлении регистрации
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            message = render_to_string('activate_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            register_message.delay(message, to_email)
            return render(request, "users/confirm_email.html")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse('website:profile'))
    else:
        return render(request, "users/false_email_token.html")


def login_view(request):
    """
    Представление входа в аккаунт,так же перенаправление.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('website:index'))
                else:
                    return render(request, "users/disabled_acc.html")
            else:
                return render(request, "users/invalid_login.html")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    """
    Представление разлогирования
    """
    logout(request)
    return redirect("website:index")


def password_change(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return render(
                request, "users/password_change_success.html"
            )
    else:
        current_user = request.user
        form = CustomPasswordChangeForm(current_user)
    return render(request, "users/password_change.html", {"form": form})


class MyPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'  # Шаблон для отправки электронной почты с ссылкой на сброс пароля
    html_email_template_name = 'users/password_reset_email.html'  # Шаблон для отправки HTML-версии электронной почты с ссылкой на сброс пароля
    from_email = os.environ.get('EMAIL_HOST_USER')
    success_url = reverse_lazy("users:password_reset_done")

    def form_valid(self, form):
        # Проверяем, существует ли email-адрес в базе данных
        email = form.cleaned_data.get('email')
        user = User.objects.filter(
            email=email).first()  # Используем filter и first вместо get с аргументом default=None
        if not user:
            return render(self.request, 'users/reset_email_false.html')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")


def password_reset_done(request):
    """
    Представление для успешного завершения сброса пароля
    """
    # Ваша логика обработки успешного завершения сброса пароля, например:
    context = {
        'message': 'Сброс пароля успешно выполнен! Проверьте почту на наличие письма подтверждение изменения пароля',
        # Сообщение, которое вы хотите отобразить на странице
    }
    return render(request, 'users/password_reset_done.html', context)


def password_reset_complete(request):
    """
    Представление для успешного завершения сброса пароля
    """
    # Ваша логика обработки успешного завершения сброса пароля, например:
    context = {
        'message': 'Ваш пароль изменен',  # Сообщение, которое вы хотите отобразить на странице
    }
    return render(request, 'users/password_reset_complete.html', context)
