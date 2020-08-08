# Generated by Django 2.2.13 on 2020-08-08 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0012_auto_20200326_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalog_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Course name in catalog')),
                ('short_name', models.CharField(blank=True, help_text='A human-friendly short name of course', max_length=255, null=True)),
                ('number', models.CharField(blank=True, help_text='include PH e.g. "PH 425"', max_length=255, null=True)),
                ('quarter_numbers', models.CharField(blank=True, help_text='e.g. Fall of Junior year = 7, comma delimit if taught at multiple stages', max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description in catalog')),
                ('publication', models.BooleanField(default=False, help_text='Course is ready for public viewing', verbose_name='Publish course')),
            ],
        ),
    ]
