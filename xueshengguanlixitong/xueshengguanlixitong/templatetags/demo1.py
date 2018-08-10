from django import template

register = template.Library()

@register.filter
def up(value):
    return value.upper()