# Generated by Django 2.2.13 on 2020-11-02 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0042_auto_20201102_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='course_topics',
            field=models.ManyToManyField(related_name='activities', to='admin_app.CourseContent'),
        ),
        migrations.AddField(
            model_name='problem',
            name='course_topics',
            field=models.ManyToManyField(related_name='problems', to='admin_app.CourseContent'),
        ),
    ]
