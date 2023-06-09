# Generated by Django 4.2 on 2023-04-13 09:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("website", "0005_service_short_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentWebsite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=250, verbose_name="Comment text")),
                (
                    "pub_date",
                    models.DateField(
                        auto_now=True, verbose_name="Comment publication date"
                    ),
                ),
                ("rating", models.IntegerField(verbose_name="Rating comment")),
                (
                    "update_date",
                    models.DateField(auto_now=True, verbose_name="Comment update date"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
