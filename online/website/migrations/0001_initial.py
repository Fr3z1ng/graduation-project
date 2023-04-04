# Generated by Django 4.2 on 2023-04-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Service name')),
                ('description', models.TextField(max_length=1000, verbose_name='Service description')),
                ('cost', models.IntegerField()),
            ],
        ),
    ]
