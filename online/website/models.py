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
    time = models.CharField(max_length=40, verbose_name="Time service", default="15 минут")

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
    text = models.TextField(max_length=250, verbose_name="Comment text")
    pub_date = models.DateField(
        verbose_name="Comment publication date", auto_now=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # добавил поле user
    update_date = models.DateField(
        verbose_name="Comment update date", auto_now=True
    )

    @staticmethod
    def get_absolute_url():
        # Возвращает URL для перенаправления после успешной обработки формы
        return reverse('website:comment')


class PhotoGallery(models.Model):
    photo_gallery = models.ImageField(
        upload_to="profile", blank=True, null=True, verbose_name="Photo gallery Image"
    )
    category = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        """
        Добавил индексы для полей таблицы price и name
        """

        indexes = [
            models.Index(fields=["photo_gallery"], name="website_photo_gallery-index"),
        ]


class StockShares(models.Model):
    name = models.CharField(max_length=50, verbose_name='Stock shares name')
    description = models.TextField(max_length=1000, verbose_name='Service description')
    cost = models.IntegerField()
    service_image = models.ImageField(
        upload_to="stock_shares_image", blank=True, null=True, verbose_name="Stock shares Image"
    )
    short_description = models.TextField(max_length=250, verbose_name='Service short description')
