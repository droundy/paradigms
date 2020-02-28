from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import admin_app.templatetags.latex_snippets

register = template.Library()

@register.filter()
def latex_with_solution(value):
    if value:
        return latex_snippets.html_with_solution(value)
    else:
        return value

@register.filter()
def latex_omit_solution(value):
    if value:
        return latex_snippets.html_omit_solution(value)
    else:
        return value
