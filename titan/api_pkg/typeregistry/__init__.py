import moonleap.resource.props as P
from moonleap import MemFun, Prop, create, create_forward, empty_rule, extend, rule
from moonleap.verbs import has

from . import props
from .resources import TypeRegistry

rules = [
    (("type-registry", has, "item"), empty_rule()),
    (("type-registry", has, "item~list"), empty_rule()),
    (("type-registry", has, "item~type"), empty_rule()),
]


@create("type-registry")
def create_type_registry(term):
    type_registry = TypeRegistry()
    return type_registry


@rule("item")
def item_created(item):
    return create_forward(":type-registry", has, item)


@rule("item~list")
def item_list_created(item_list):
    return create_forward(":type-registry", has, item_list)


@rule("item~type")
def item_type_created(item_type):
    return create_forward(":type-registry", has, item_type)


@extend(TypeRegistry)
class ExtendTypeReg:
    items = P.children(has, "item")
    item_lists = P.children(has, "item~list")
    item_types = P.children(has, "item~type")
    get_item_by_name = MemFun(props.get_item_by_name)
