# Generated by Django 2.2.13 on 2020-08-12 22:27

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0016_auto_20200812_1353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseastaught',
            options={'verbose_name': 'Course as taught', 'verbose_name_plural': 'Courses as taught'},
        ),
        migrations.AddField(
            model_name='courseastaught',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='xxx', editable=False, populate_from='year'),
            preserve_default=False,
        ),
    ]