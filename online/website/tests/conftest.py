import pytest
from website.models import Service, CommentWebsite, Profile
from django.contrib.auth import get_user_model


@pytest.fixture
def users(faker):
    users = []
    user_model = get_user_model()
    new_user = user_model.objects.create_user(username='newuser', password='12345')
    users.append(user_model.objects.get(username=new_user))
    for i in range(9):
        username = faker.word()
        password = '12345'
        user_model.objects.create_user(username=username, password=password)
        users.append(user_model.objects.get(username=username))
    return users


@pytest.fixture
def create_data_service(faker):
    data = []
    for i in range(10):
        data.append(
            Service(
                pk=i,
                name=faker.word(),
                description=faker.text(max_nb_chars=1000),
                cost=faker.random_int(min=0, max=1000),
                # вместо реального изображения здесь используется None
                service_image="default.JPG",
                pros=faker.text(max_nb_chars=1000),
                minuses=faker.text(max_nb_chars=1000),
                short_description=faker.text(max_nb_chars=250),
                time=faker.random_element(elements=("15 минут", "30 минут", "1 час", "2 часа")),
                slug=faker.slug(),
            )
        )
    return Service.objects.bulk_create(data)


@pytest.fixture
def create_comments(faker, users):
    comments = []
    comment_id = 0
    for user in users:
        comment_id += 1
        comments.append(
            CommentWebsite(
                id=comment_id,
                text=faker.text(max_nb_chars=250),
                pub_date=faker.date(),
                user=user,
                update_date=faker.date(),
            )
        )
    return CommentWebsite.objects.bulk_create(comments)


@pytest.fixture
def create_profiles(faker, users):
    profile_id = 0
    profiles = []
    for user in users:
        profile_id += 1
        profiles.append(
            Profile(
                id=profile_id,
                first_name=faker.word(),
                last_name=faker.word(),
                profile_image="default.JPG",
                phone_number='+375(33)343-26-01',
                user=user,
            )
        )
    return Profile.objects.bulk_create(profiles)
