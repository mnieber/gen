from django import template

from app.tr import tr

register = template.Library()


@register.filter(name="tr")
def tr_value(value):
    return tr(value)
