from django import template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

register = template.Library()

@register.filter
def syntax_highlight(text, language):
	return highlight(text, get_lexer_by_name(language), HtmlFormatter())
