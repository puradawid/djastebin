# ./apps/pastes/templatetags/syntax_highlighting.pyy

#Django imports
from django import template

#Pygments imports
from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

register = template.Library()

#Filters as methods

@register.filter
def syntax_highlight(text, language):
    if language != 'NONE':
        return highlight(text, get_lexer_by_name(language.lower()), HtmlFormatter())
    return '<pre>' + text + '</pre>'

@register.filter
def get_css(text):
	return HtmlFormatter().get_style_defs("pre")
