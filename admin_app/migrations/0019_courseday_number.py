# Generated by Django 2.2.13 on 2020-08-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0018_courseday'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseday',
            name='number',
            field=models.PositiveIntegerField(default=1000),
        ),
    ]
