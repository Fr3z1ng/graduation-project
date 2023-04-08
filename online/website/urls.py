from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "website"
urlpatterns = [
                  path("", views.index, name="index"),
                  path("profile", views.profile, name="profile"),
                  path("service", views.service_view, name="service"),
                  path("service/<int:pk>", views.service_info, name="service_info"),
              ]
