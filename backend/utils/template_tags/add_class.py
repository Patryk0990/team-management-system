from django import template
from django.utils.html import escape

register = template.Library()


@register.filter
def add_class(element, css_class):
    classes = element.field.widget.attrs.get('class', '')
    updated_classes = f'{classes} {css_class}'
    element.field.widget.attrs['class'] = escape(updated_classes)
    return element
