from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from admin_app.choices import *
from admin_app.models import Pages
from django.db.models import Q

register = template.Library()

# The following tag will display a list of hrefs for inclusion in a 
# standard bootstrap nav dropdown list
# The list is populated by querying the boolean field whitepaper for "1", and the choice field
# whitepaper_category using the value passed from the tag

@register.filter(needs_autoescape=True)
def whitepaperdropdownlist(value, autoescape=True):
    if value:
        links = Pages.objects.filter(Q(whitepaper__exact=1) and Q(whitepaper_category__exact=value)).order_by('title')
        link_list = ''
        for link in links:
            link_list += '<a class="dropdown-item" href="/whitepaper/' + link.slug + '">' + link.title + '</a>'
        return mark_safe(link_list)
    else:
        return value

@register.filter(needs_autoescape=True)
def whitepaperlist(value, autoescape=True):
    if value:
        links = Pages.objects.filter(Q(whitepaper__exact=1) and Q(whitepaper_category__exact=value)).order_by('title')
        link_list = '<ul>'
        for link in links:
            link_list += '<li><a class="dropdown-item" href="/whitepaper/' + link.slug + '">' + link.title + '</a></li>'
        link_list = link_list + '</ul>'
        return mark_safe(link_list)
    else:
        return value