import pytest
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from unittest.mock import patch, MagicMock
from users.token import account_activation_token

User = get_user_model()


# @pytest.mark.django_db
# def test_register_view_post_valid(client, user_data, mock_register_message):
#     response = client.post(reverse("users:register"), user_data)
#     assert response.status_code == 200
#     user = User.objects.filter(email="test@example.com").first()
#     message = render_to_string(
#         "activate_email.html",
#         {
#             "user": user,
#             "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#             "token": account_activation_token.make_token(user),
#         },
#     )
#     to_email = user_data.get("email")
#     assert mock_register_message.assert_called_once_with(message, to_email)
#     assert user is not None
#     assert not user.is_active


# @pytest.mark.django_db
# def test_registration_flow(client, mock_register_message):
#     response = client.post(reverse('users:register'), data)
#     assert response.status_code == 302  # Проверяем, что пользователь успешно создан
#     user = User.objects.get(username=data['username'])
#     assert not user.is_active
#     assert mock_register_message.called_once_with(
#         message=MagicMock(),
#         email=data['email'],
#     )
#     # Получаем ссылку на активацию токена из последнего отправленного сообщения
#     assert len(mail.outbox) == 1
#     message = mail.outbox[0].message()
#     uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#     token = account_activation_token.make_token(user)
#     activation_url = reverse('users:activate', args=[uidb64, token])
#
#     # Переходим по ссылке на активацию токена
#     response = client.get(activation_url)
#
#     # Проверяем, что пользователь был активирован и перенаправлен на страницу профиля
#     assert response.status_code == 302
#     user.refresh_from_db()
#     assert user.is_active
#     assert response.url == reverse('website:profile')


@pytest.mark.django_db
def test_login(client, user):
    data = {
        'username': 'newuser',
        'password': 'alex7229',
    }
    response = client.post(reverse("users:login"), data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout(client, user):
    client.login(username='newuser', password='alex7229')
    response = client.post(reverse("users:logout"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_password_change(client, user):
    client.login(username='newuser', password='alex7229')
    user_model = get_user_model()
    new_user = user_model.objects.get(username='newuser')
    old_password_hash = new_user.password
    data = {
        'old_password': 'alex7229',
        'new_password1': 'alex7229722',
        'new_password2': 'alex7229722',
    }
    response = client.post(reverse("users:password-change"), data)
    new_user.refresh_from_db()
    assert response.status_code == 200
    assert new_user.password != old_password_hash


@pytest.mark.django_db
def test_password_change_error(client, user):
    client.login(username='newuser', password='alex7229')
    user_model = get_user_model()
    new_user = user_model.objects.get(username='newuser')
    old_password_hash = new_user.password
    data = {
        'old_password': 'alex7229',
        'new_password1': 'alex722972',
        'new_password2': 'alex7229722',
    }
    response = client.post(reverse("users:password-change"), data)
    new_user.refresh_from_db()
    assert response.status_code == 200
    assert new_user.password == old_password_hash


@pytest.mark.django_db
def test_reset_done(client, user):
    response = client.get(reverse("users:password_reset_done"))
    assert response.status_code == 200
