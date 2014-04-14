from django import template
import re

register = template.Library()

@register.filter
def url_username(text):
    return re.sub(r'(?: |^)@([\w_-]+)', r'<a href="/u/\1">@\1</a>', text)