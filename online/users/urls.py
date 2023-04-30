from .views import MyPasswordResetView, PasswordResetConfirmView
from django.urls import path
from . import views


app_name = "users"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password-change/", views.password_change, name="password-change"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    ]
