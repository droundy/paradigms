# Generated by Django 2.2.13 on 2020-08-14 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0019_courseday_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseday',
            name='taught',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_app.CourseAsTaught'),
            preserve_default=False,
        ),
    ]
