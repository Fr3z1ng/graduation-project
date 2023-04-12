from django.urls import path
from . import views

app_name = "booking"
urlpatterns = [
    path('booking', views.booking, name='booking'),
    path('booking_day', views.booking_day, name='booking_day'),
    path('booking_day/<int:service_id>', views.booking_day, name='booking_day'),
    path('booking-submit', views.bookingSubmit, name='bookingSubmit'),
    path('user-update/<int:id>', views.userUpdate, name='userUpdate'),
    path('user-update-submit/<int:id>', views.userUpdateSubmit, name='userUpdateSubmit'),
    path('remove/<int:id>', views.remove, name='remove'),
]
