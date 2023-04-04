from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path, reverse_lazy
from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
