from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name='Service name')
    description = models.TextField(max_length=1000, verbose_name='Service description')
    cost = models.IntegerField()
    service_image = models.ImageField(
        upload_to="service_image", blank=True, null=True, verbose_name="Service Image"
    )
    pros = models.TextField(max_length=1000, verbose_name='Service plus description')
    minuses = models.TextField(max_length=1000, verbose_name='Service minus description')
    short_description = models.TextField(max_length=250, verbose_name='Service short description')

    def __str__(self):
        return self.name


class Profile(models.Model):
    first_name = models.CharField(max_length=25, verbose_name='Profile first_name')
    last_name = models.CharField(max_length=25, verbose_name='Profile last_name')
    profile_image = models.ImageField(
        upload_to="profile", blank=True, null=True, verbose_name="Profile Image"
    )
    phone_number = models.CharField(max_length=20, verbose_name='Profile phone_number')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.first_name


class CommentWebsite(models.Model):
    text = models.CharField(max_length=250, verbose_name="Comment text")
    pub_date = models.DateField(
        verbose_name="Comment publication date", auto_now=True
    )
    rating = models.IntegerField(verbose_name="Rating comment")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # добавил поле user
    update_date = models.DateField(
        verbose_name="Comment update date", auto_now=True
    )

    def get_absolute_url(self):
        # Возвращает URL для перенаправления после успешной обработки формы
        return reverse('website:comment')
