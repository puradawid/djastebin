# ./apps/pastes/templatetags/syntax_highlighting.pyy

#Django imports
from django import template

#Pygments imports
from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.lexers.special import TextLexer

register = template.Library()

#Filters as methods

@register.filter
def syntax_highlight(text, syntax):
    if syntax.lower() == 'none':
        lexer = TextLexer()
    else:
        lexer = get_lexer_by_name(syntax.lower()) 
    return highlight(text, lexer, HtmlFormatter(linenos='table'))


@register.filter
def get_css(text):
	return HtmlFormatter(linenos='table').get_style_defs("pre")
