from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    nickname = forms.CharField(max_length=30, required=True, help_text='Required.')
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Your password can\'t be too similar to your other personal information. Your password must contain at least 8 characters. Your password can\'t be a commonly used password. Your password can\'t be entirely numeric.'
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.'
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + (
            'email', 'nickname', 'password1', 'password2',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Создал кастомную форму для добавления функционала смены пароля
    """

    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:success_change")

    def clean(self):
        """
        при совпадении нового пароля со старым выскакивает ошибка
        """
        cleaned_data = super().clean()
        user = self.user
        new = cleaned_data.get("new_password1")
        if user.check_password(new):
            raise ValidationError("Новый пароль совпадает со старым")
