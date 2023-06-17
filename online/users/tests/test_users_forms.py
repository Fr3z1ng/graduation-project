import pytest
from users.forms import CustomUserCreationForm, CustomPasswordChangeForm


@pytest.mark.django_db
def test_custom_user_creation_form_valid(user_data):
    """
    Проверяем, что форма валидна, если переданы правильные данные
    """
    form = CustomUserCreationForm(data=user_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_change_password_form_valid(password_data, user):
    """
    Проверяем, что форма валидна, если переданы правильные данные
    """
    form = CustomPasswordChangeForm(data=password_data, user=user)
    assert form.is_valid()
