from django.template import Library
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from markdown import markdown as render_markdown

register = Library()


@register.filter
def markdown(s):
    return mark_safe(render_markdown(force_text(s)))
