# Generated by Django 2.2.13 on 2020-11-02 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0041_auto_20201102_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecontent',
            name='number',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]