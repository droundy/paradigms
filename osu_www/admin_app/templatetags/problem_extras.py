from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
def problemtopicbuttons(value, autoescape=True):
    if value:
        topic_list = value.strip().rstrip(",").split(",")
        topic_list = map(str.strip, topic_list)
        buttons = ''
        for topic in topic_list:
            buttons += '<a class="badge badge-secondary" href="/search/keyword/' + topic + '">' + topic + '</a> '
        return mark_safe(buttons)
    else:
        return value