from django import template

register = template.Library()

@register.filter
def hash(value, key):
    " Returns value[key] "
    return value[key]
