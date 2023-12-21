from django import template

register = template.Library()


@register.filter
def add_attr(element, attr):
    attrs = {}
    attr_name, attr_value = attr.split('=', 1)
    attrs[attr_name] = attr_value
    element.field.widget.attrs.update(attrs)
    return element
