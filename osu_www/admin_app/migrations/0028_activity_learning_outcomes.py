# Generated by Django 2.2.13 on 2020-08-17 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0027_auto_20200817_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='learning_outcomes',
            field=models.ManyToManyField(related_name='activities', to='admin_app.CourseLearningOutcome'),
        ),
    ]
