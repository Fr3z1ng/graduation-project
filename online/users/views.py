from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from .forms import CustomUserCreationForm, LoginForm
from django.core.mail import send_mail


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
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('activate_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(
                mail_subject,
                message,
                'beste1997@mail.ru',
                [to_email],
                fail_silently=False,
            )
            return HttpResponse('Please confirm your email address to complete the registration')
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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def login_view(request):
    """
    Представление входа в аккаунт,так же перенаправление.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        next_url = request.POST.get("next")  # необходимо для перенаправление на ресурс
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('website:index'))
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    """
    Представление разлогирования
    """
    logout(request)
    return redirect("website:index")
