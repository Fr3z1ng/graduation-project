from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name='Service name')
    description = models.TextField(max_length=1000, verbose_name='Service description')
    cost = models.IntegerField()

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
