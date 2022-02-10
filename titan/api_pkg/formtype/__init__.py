import moonleap.resource.props as P
from moonleap import create, empty_rule, extend, kebab_to_camel, rule, u0
from moonleap.verbs import has
from titan.api_pkg.itemtype.resources import ItemType

from . import props
from .resources import FormType


@create("item~form-type")
def create_form_type(term, block):
    name = kebab_to_camel(term.data)
    form_type = FormType(
        name=u0(name) + "Form",
        type_name=u0(name),
    )
    return form_type


@rule("item~form-type")
def form_type_created(form_type):
    props.get_or_create_form_type_spec(form_type)


rules = [(("item~type", has, "item~form-type"), empty_rule())]


@extend(ItemType)
class ExtendItemType:
    form_type = P.child(has, "item~form-type")
