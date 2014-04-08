# ./apps/pastes/templatetags/syntax_highlighting.pyy

#Django imports
from django import template

#Pygments imports
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

register = template.Library()

#Filters as methods

@register.filter
def syntax_highlight(text, language):
    if language != None
        return highlight(text, get_lexer_by_name(language), HtmlFormatter())
    return text
