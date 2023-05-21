from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Service(models.Model):
    """
    Модель услуг которые предоставляет мастер
    """

    name = models.CharField(max_length=50, verbose_name="Название услуги")
    description = models.TextField(max_length=1000, verbose_name="Описание услуги")
    cost = models.IntegerField()
    service_image = models.ImageField(
        upload_to="service_image", blank=True, null=True, verbose_name="Service Image"
    )
    pros = models.TextField(max_length=1000, verbose_name="Описание плюсов")
    minuses = models.TextField(max_length=1000, verbose_name="Описание минусов")
    short_description = models.TextField(
        max_length=250, verbose_name="Короткое описание"
    )
    time = models.CharField(
        max_length=40, verbose_name="Длительность услуги", default="15 минут"
    )
    slug = models.CharField(
        max_length=50, verbose_name="Сокращенное название услуги", default=""
    )

    def __str__(self):
        """
        строковое представление объектов Service
        """
        return self.name


class Profile(models.Model):
    """
    Модель профиля для пользователя
    """

    first_name = models.CharField(max_length=25, verbose_name="Имя пользователя")
    last_name = models.CharField(max_length=25, verbose_name="Фамилия пользователя")
    profile_image = models.ImageField(
        upload_to="profile", blank=True, null=True, verbose_name="Profile Image"
    )
    phone_number = models.CharField(
        max_length=20, verbose_name="Номер телефона пользователя"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        строковое представление объектов Profile
        """
        return self.first_name


class CommentWebsite(models.Model):
    """
    Модель отзывов о мастере
    """

    text = models.TextField(max_length=250, verbose_name="Comment text")
    pub_date = models.DateField(verbose_name="Comment publication date", auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    update_date = models.DateField(verbose_name="Comment update date", auto_now=True)

    @staticmethod
    def get_absolute_url():
        """
        При совершении действий возвращает по пути указанной в reverse
        """
        return reverse("website:comment")


class PhotoGallery(models.Model):
    """
    Модель фотогалереи вебсайта
    """

    photo_gallery = models.ImageField(
        upload_to="profile", blank=True, null=True, verbose_name="Photo gallery Image"
    )
    category = models.ForeignKey(
        Service, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        """
        Добавил индексы для поле таблицы photo_gallery
        """

        indexes = [
            models.Index(fields=["photo_gallery"], name="website_photo_gallery-index"),
        ]
