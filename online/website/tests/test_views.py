import pytest
from django.urls import reverse
import random
from website.models import CommentWebsite, Profile
from django.utils import timezone

@pytest.mark.parametrize('param', [
    ('website:index'),
    ('website:profile'),
    ('website:contact'),
    ('website:service'),
    ('website:comment'),
    ('website:photo-gallery')
])
@pytest.mark.usefixtures('create_data_service', 'users')
@pytest.mark.django_db
def test_render_views(client, param, users):
    client.login(username='newuser', password='12345')
    resp = client.get(reverse(param))
    assert resp.status_code == 200


@pytest.mark.parametrize('param', [
    ('website:service_info'),
])
@pytest.mark.usefixtures('create_data_service', 'users')
@pytest.mark.django_db
def test_service_info_view(client, param):
    client.login(username='newuser', password='12345')
    response = client.get(reverse(param, kwargs={'pk': 1}))
    assert response.status_code == 200


@pytest.mark.usefixtures('create_comments', 'users')
@pytest.mark.django_db
def test_comment_update(client, users):
    client.login(username='newuser', password='12345')
    random_number = random.randint(1, 10)
    response = client.get(reverse('website:comment-update', kwargs={'pk': random_number}))
    comment = CommentWebsite.objects.get(id=random_number)
    assert response.status_code == 200
    assert CommentWebsite.objects.count() == 10
    assert response.context['comment'] == comment
    updated_text = 'Updated test comment'
    response = client.post(reverse('website:comment-update', kwargs={'pk': comment.pk}), {
        'text': updated_text
    })
    assert response.status_code == 302
    comment.refresh_from_db()
    assert comment.text == updated_text
    assert CommentWebsite.objects.count() == 10


@pytest.mark.usefixtures('create_comments', 'users')
@pytest.mark.django_db
def test_comment_delete(client, users):
    client.login(username='newuser', password='12345')
    random_number = random.randint(1, 10)
    response = client.get(reverse('website:comment-delete', kwargs={'pk': random_number}))
    comment = CommentWebsite.objects.get(id=random_number)
    assert response.status_code == 200
    assert CommentWebsite.objects.count() == 10
    assert response.context['comment'] == comment
    response = client.post(reverse('website:comment-delete', kwargs={'pk': comment.pk}))
    assert response.status_code == 302
    assert CommentWebsite.objects.count() == 9


@pytest.mark.usefixtures('create_profiles', 'users')
@pytest.mark.django_db
def test_profile_edit(client):
    client.login(username='newuser', password='12345')
    new_data = {
        "first_name": "New First Name",
        "last_name": "New Last Name",
        "phone_number": "1234567890",
    }
    profile = Profile.objects.first()
    response = client.post(reverse("website:profile_edit"), data=new_data)
    assert Profile.objects.count() == 10
    assert response.status_code == 302
    assert response.url == reverse("website:profile")
    profile.refresh_from_db()
    assert profile.first_name == new_data["first_name"]
    assert profile.last_name == new_data["last_name"]
    assert profile.phone_number == new_data["phone_number"]
    assert Profile.objects.count() == 10


@pytest.mark.usefixtures('users')
@pytest.mark.django_db
def test_comment_add(client):
    client.login(username='newuser', password='12345')
    response = client.get(reverse('website:comment_add'))
    assert CommentWebsite.objects.count() == 0
    assert response.status_code == 200
    new_data = {
        "text": "New text",
        "pub_date": timezone.now(),
        "update_date": timezone.now()
    }
    response = client.post(reverse('website:comment_add'), data=new_data)
    assert response.status_code == 302
    assert CommentWebsite.objects.count() == 1
    assert response.url == reverse("website:comment")
    comment = CommentWebsite.objects.last()
    assert comment.text == new_data["text"]

