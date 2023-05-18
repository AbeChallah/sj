from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def bootstrap(form):
    html = form.as_p()
    html = html.replace('<label', '<label class="form-label"')
    html = html.replace('<input', '<input class="form-control"')
    html = html.replace('<select', '<select class="form-select"')
    html = html.replace('<textarea', '<textarea class="form-control"')
    return mark_safe(html)
