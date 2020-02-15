from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='trimtob')


# topic_list = activity.topics.strip().rstrip(",").split(",")
# topic_list = map(str.strip, topic_list)


# def cut(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, '')

# Used to repair type_of_beast formatting
# {{ activity.type_of_beast|trimtob }}
def trimtob(value):
    if value:
        tob = value.strip("('")
        tob = tob.strip("'),")
        return tob
    else:
        return value

@register.filter(needs_autoescape=True)
def tagbuttons(value, autoescape=True):
    if value:
        topic_list = value.strip().rstrip(",").split(",")
        topic_list = map(str.strip, topic_list)
        buttons = ''
        for topic in topic_list:
            buttons += '<a class="badge badge-secondary" href="/search/keyword/' + topic + '">' + topic + '</a> '
        return mark_safe(buttons)
    else:
        return value