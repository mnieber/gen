import moonleap.resource.props as P
from moonleap import create, empty_rule, extend, kebab_to_camel, kebab_to_snake
from moonleap.verbs import receives
from titan.django_pkg.module import Module

from .resources import Form


@create(["form"])
def create_form(term, block):
    item_name = kebab_to_camel(term.data)
    item_name_snake = kebab_to_snake(term.data)
    form = Form(item_name=item_name, item_name_snake=item_name_snake)
    return form


rules = [(("module", receives, "form"), empty_rule)]


@extend(Module)
class ExtendModule:
    forms = P.children(receives, "form")
