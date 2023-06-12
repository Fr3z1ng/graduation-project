# import pytest
# from website.forms import ProfileModelForm
# from website.models import Profile
#
#
# @pytest.mark.django_db
# def test_profile_form_valid(client):
#     # Создаем данные для формы
#     data = {
#         'first_name': 'John',
#         'last_name': 'Doe',
#         'phone_number': '1234567890',
#         'profile_image': '',
#     }
#
#     # Создаем экземпляр формы
#     form = ProfileModelForm(data=data)
#
#     # Проверяем, что форма валидна
#     assert form.is_valid()
#
#     # Сохраняем данные в базу данных
#     obj = form.save()
#
#     # Проверяем, что объект сохранен в базе данных
#     assert Profile.objects.count() == 1
#
#     # Проверяем, что поля объекта заполнены корректно
#     assert obj.first_name == "John"
#     assert obj.last_name == "Doe"
#     assert obj.phone_number == "1234567890"
