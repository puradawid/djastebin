from atexit import register
from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    return int(value) - int(arg)

@register.filter
def visibility_convert(value):    
    if value == 'PUBLIC':
        return 'fa-unlock'
    elif value == 'UNLISTED':
        return 'fa-lock'
    else:
        return 'fa-ban'

@register.filter
def short_if(value, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]

    if value == arg_list[0]:
        return arg_list[1]
    else:
        return arg_list[2]
