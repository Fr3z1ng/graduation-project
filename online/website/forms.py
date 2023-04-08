from django import forms
from django.forms import Textarea
from django.views.generic.edit import FormView

from .models import Profile


class ProfileModelForm(forms.ModelForm):
    """
    Форма для ввода и редактирования комментария
    """
    profile_image = forms.ImageField(label='Фото профиля', required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_image', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Введите фамилию'}),
            'phone_number': forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Введите номер телефона'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'number_phone': 'Мобильный номер',
        }
