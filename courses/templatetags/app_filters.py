from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    foo = str(dictionary[key]).strip('[]\'')
    return foo
