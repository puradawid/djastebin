from atexit import register
from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    return int(value) - int(arg)