from unittest.mock import patch
from django.contrib.auth.models import User
import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def mock_register_message():
    with patch("users.tasks.register_message.delay") as mock_delay:
        yield mock_delay


@pytest.fixture
def user_data():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
    }
    return user_data


@pytest.fixture
def password_data():
    password_data = {
         'old_password': 'alex7229',
        'new_password1': 'alex7229722',
        'new_password2': 'alex7229722',
    }
    return password_data


@pytest.fixture
def user():
    user_model = get_user_model()
    return user_model.objects.create_user(username='newuser', password='alex7229')
