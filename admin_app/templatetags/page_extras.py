from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from admin_app.choices import *
from admin_app.models import Pages
from django.db.models import Q

register = template.Library()

# The following tag will display a list of hrefs for inclusion in a 
# standard bootstrap nav dropdown list
# The list is populated from the Pages database using the whitepapers field
# This can be filtered using additional fields or alternate queries as needed
# Possibly use like this in a template {{ 'whitepaper'|pagedropdownlist }}
# Where "whitepaper" is the boolean field you want to query? Not sure yet.
# 

@register.filter(needs_autoescape=True)
def pagedropdownlist(value, autoescape=True):
    if value:
        links = Pages.objects.filter(Q(whitepaper__exact=1)).order_by('title')
        link_list = ''
        for link in links:
            link_list += '<a class="dropdown-item" href="/whitepaper/' + link.slug + '">' + link.title + '</a>'
        return mark_safe(link_list)
    else:
        return value