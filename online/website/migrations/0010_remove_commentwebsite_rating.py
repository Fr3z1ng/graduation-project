# Generated by Django 4.2 on 2023-04-26 18:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0009_alter_commentwebsite_text"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="commentwebsite",
            name="rating",
        ),
    ]
