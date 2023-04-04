from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50, verbose_name='Service name')
    description = models.TextField(max_length=1000, verbose_name='Service description')
    cost = models.IntegerField()

    def __str__(self):
        return self.name
