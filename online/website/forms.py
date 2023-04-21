from django import forms
from django.forms import Textarea
from django.views.generic.edit import FormView

from .models import Profile, CommentWebsite


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


class CommentModelForm(forms.ModelForm):
    """
    Форма для ввода и редактирования комментария
    """

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 0 or rating > 10:
            raise forms.ValidationError("Only possitive number and less 11 are allowed")
        return rating

    class Meta:
        model = CommentWebsite
        exclude = [
            "pub_date",
            "update_date",
            "user",
        ]
        widgets = ({"text": Textarea(attrs={"cols": 80, "rows": 20})},)
        labels = (
            {
                "text": "Comment text",
            },
        )
        help_texts = {"text": "Оцените нас,пожалуйста "}
