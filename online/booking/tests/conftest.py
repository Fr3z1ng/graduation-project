from datetime import timezone

import pytest
from django.contrib.auth import get_user_model
from website.models import Service
from booking.models import Appointment
from datetime import timedelta
import random
from django.utils import timezone


@pytest.fixture
def user():
    user_model = get_user_model()
    return user_model.objects.create_user(id=1, username='newuser', password='alex7229')


@pytest.fixture
def create_data_service(faker):
    service = Service.objects.create(
        pk=1,
        name=faker.word(),
        description=faker.text(max_nb_chars=1000),
        cost=faker.random_int(min=0, max=1000),
        service_image="default.JPG",
        pros=faker.text(max_nb_chars=1000),
        minuses=faker.text(max_nb_chars=1000),
        short_description=faker.text(max_nb_chars=250),
        time=faker.random_element(elements=("15 минут", "30 минут", "1 час", "2 часа")),
        slug=faker.slug(),
    )
    return service


@pytest.fixture
def create_data_appoinment(faker, user, create_data_service):
    day = faker.date_between(start_date='today', end_date='+30d')
    time = faker.random_element(elements=('10.00', '12.00', '14.00', '16.00'))
    time_ordered = timezone.now() - timedelta(days=random.randint(1, 7))
    appoinment = Appointment.objects.create(
        user=user,
        service=create_data_service,
        day=day,
        time=time,
        time_ordered=time_ordered
    )
    return appoinment
