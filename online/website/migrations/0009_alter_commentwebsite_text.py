# Generated by Django 4.2 on 2023-04-25 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_stockshares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentwebsite',
            name='text',
            field=models.TextField(max_length=250, verbose_name='Comment text'),
        ),
    ]
