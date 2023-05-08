from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.urls import reverse_lazy


class CustomUserCreationForm(UserCreationForm):
    """
    Форма создания пользователя
    """

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"size": "65", "style": "height: 60px;"}),
    )
    username = forms.CharField(
        label="Введите никнейм",
        widget=forms.TextInput(attrs={"class": "my-input"}),
        help_text="Никнейм не должен содержать специальные символы",
    )
    password1 = forms.CharField(
        label="Введите пароль",
        widget=forms.PasswordInput(attrs={"class": "my-input"}),
        help_text="Ваш пароль не может состоять полностью из цирф и должен содержать не менее 8 символов",
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "my-input"}),
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        """
        Форма для ввода данных профиля
        """
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email


class LoginForm(forms.Form):
    """
    Форма для входа в аккаунт
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Создал кастомную форму для добавления функционала смены пароля
    """

    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:success_change")

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ["old_password", "new_password1", "new_password2"]:
            self.fields[fieldname].help_text = None

    def clean(self):
        """
        при совпадении нового пароля со старым выскакивает ошибка
        """
        cleaned_data = super().clean()
        user = self.user
        new = cleaned_data.get("new_password1")
        if user.check_password(new):
            raise ValidationError("Новый пароль совпадает со старым")
