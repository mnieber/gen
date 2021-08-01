import moonleap.resource.props as P
from moonleap import extend, kebab_to_camel, kebab_to_snake, tags
from moonleap.verbs import receives
from moonleap_django.module import Module

from .resources import Form


@tags(["form"])
def create_form(term, block):
    item_name_camel = kebab_to_camel(term.data)
    item_name_snake = kebab_to_snake(term.data)
    form = Form(item_name_camel=item_name_camel, item_name_snake=item_name_snake)
    return form


empty_rules = [("module", receives, "form")]


@extend(Module)
class ExtendModule:
    forms = P.children(receives, "form")
