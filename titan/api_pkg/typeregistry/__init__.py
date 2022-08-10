import moonleap.resource.props as P
from moonleap import MemFun, create, create_forward, empty_rule, extend, rule
from moonleap.verbs import has

from . import props
from .resources import TypeRegistry

rules = [
    (("type-registry", has, "item~type"), empty_rule()),
    (("type-registry", has, "item~form-type"), empty_rule()),
]

_type_registry = TypeRegistry()


def get_type_reg():
    return _type_registry


@create("type-registry")
def create_type_registry(term):
    return _type_registry


@rule("item~type")
def item_type_created(item_type):
    return create_forward(":type-registry", has, item_type)


@rule("item~form-type")
def item_form_type_created(item_form_type):
    return create_forward(":type-registry", has, item_form_type)


@extend(TypeRegistry)
class ExtendTypeReg:
    item_types = P.children(has, "item~type")
    item_form_types = P.children(has, "item~form-type")
    get_item_type_by_name = MemFun(props.get_item_type_by_name)
