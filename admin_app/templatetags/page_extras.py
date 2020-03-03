from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from admin_app.choices import *
from admin_app.models import Pages

register = template.Library()
