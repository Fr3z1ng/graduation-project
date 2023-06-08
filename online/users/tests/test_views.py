# from django import urls
# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
# from users.views import register
# import pytest
#
#
# @pytest.mark.django_db
# def test_user_signup(client):
#     user_model = get_user_model()
#     assert user_model.objects.count() == 0
#     data = {
#         "username": 'fr3z1ng',
#         "password": '12345'
#     }
#     response = client.post(reverse("website:profile_edit"), data=data)
#
#     assert response.status_code == 302
import pytest
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from users.views import register, activate
from users.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_register_view_get(client):
    response = client.get(reverse("users:register"))
    assert response.status_code == 200
    assert "form" in response.context
    assert isinstance(response.context["form"], CustomUserCreationForm)


@pytest.mark.django_db
def test_register_view_post_valid(client):

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
    }
    response = client.post(reverse("users:register"), user_data)
    assert response.status_code == 200
    user = User.objects.filter(email="test@example.com").first()
    assert user is not None
    assert not user.is_active
