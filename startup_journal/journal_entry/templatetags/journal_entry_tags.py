from django import template
from django.utils.safestring import mark_safe
import markdown
from ..models import Entry

register = template.Library()

@register.simple_tag
def tag_objects():
    return

@register.inclusion_tag('tags.html')
def get_tags():
    tag_objects = Entry.tags.all()
    return {'tag_objects' : tag_objects}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
