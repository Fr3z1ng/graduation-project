import pytest
from django.urls import reverse
from booking.models import Appointment
import datetime


@pytest.mark.usefixtures('create_data_service', 'user')
@pytest.mark.django_db
def test_booking(client, user, create_data_service):
    client.login(username='newuser', password='12345')
    form_data = {
        'service_id': create_data_service.pk,
    }
    response = client.post(reverse('booking:booking'), form_data)
    assert response.status_code == 302
    assert Appointment.objects.count() == 0


@pytest.mark.usefixtures('create_data_service', 'user')
@pytest.mark.django_db
def test_booking_day(client, user, create_data_service):
    client.login(username='newuser', password='12345')
    form_data = {
        'service_id': create_data_service.pk,
        'day': datetime.date.today(),
    }
    response = client.post(reverse('booking:booking_day'), form_data)
    assert response.status_code == 302
    assert Appointment.objects.count() == 0


# @pytest.mark.usefixtures('create_data_service', 'user')
# @pytest.mark.django_db
# def test_booking_submit(client, user, create_data_service):
#     c = Client()
#     c.login(username='newuser', password='alex7229')
#     now = datetime.now()
#     time_str = now.strftime("%H:%M")
#     data = {'day': '12-12-2022'}
#     day_str = data['day']
#     day_obj = datetime.strptime(day_str, '%d-%m-%Y').date()
#     form_data = {
#         'user': user.pk,
#         'service': create_data_service.id,
#         'day': day_obj,
#         'time': time_str,
#         'time_ordered': now,
#     }
#     print(form_data)
#     response = c.post(reverse('booking:bookingSubmit'), form_data)
#     assert response.status_code == 302
#     assert Appointment.objects.count() == 1


@pytest.mark.usefixtures('create_data_appoinment', 'user')
@pytest.mark.django_db
def test_appointment_remove(client, user):
    client.login(username='newuser', password='alex7229')
    appointment = Appointment.objects.first()
    assert Appointment.objects.count() == 1
    resp = client.post(reverse('booking:remove', args=[appointment.id]))
    assert resp.status_code == 302
    assert Appointment.objects.count() == 0


@pytest.mark.usefixtures('user')
@pytest.mark.django_db
def test_user_record(client, user):
    client.login(username='newuser', password='alex7229')
    resp = client.post(reverse('booking:user_record'))
    assert resp.status_code == 200


@pytest.mark.usefixtures('user')
@pytest.mark.django_db
def test_history_user(client, user):
    client.login(username='newuser', password='alex7229')
    resp = client.post(reverse('booking:history_user'))
    assert resp.status_code == 200
