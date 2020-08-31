"""
WSGI config for osu_www_student project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'osu_www_student.settings')
os.environ['MYSQL_PWD'] = 'hai8Shei4koo#noo:pha4ookiw1Eip'

application = get_wsgi_application()
