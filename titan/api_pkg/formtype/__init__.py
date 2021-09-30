import moonleap.resource.props as P
from moonleap import create, empty_rule, extend, kebab_to_camel, kebab_to_snake, rule
from moonleap.verbs import has
from titan.api_pkg.itemtype.resources import ItemType

from . import props
from .resources import FormType


@create("item~form-type")
def create_form_type(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    form_type = FormType(
        name=name,
        name_snake=name_snake,
    )
    return form_type


@rule("item~form-type")
def form_type_created(form_type):
    props.get_or_create_form_type_spec(form_type.name)


rules = [(("item~type", has, "item~form-type"), empty_rule())]


@extend(ItemType)
class ExtendItemType:
    form_type = P.child(has, "item~form-type")
