import moonleap.resource.props as P
from moonleap import create, create_forward, empty_rule, extend, rule
from moonleap.session import get_session
from moonleap.utils.case import camel_to_kebab, l0
from moonleap.verbs import has
from titan.types_pkg.pkg.load_type_specs import load_type_specs

from .resources import TypeRegistry

rules = {
    ("project", has, ":type-registry"): empty_rule(),
    ("type-registry", has, "generic-item"): empty_rule(),
    ("type-registry", has, "item"): empty_rule(),
    ("type-registry", has, "item~list"): empty_rule(),
    ("project", has, "type-registry"): empty_rule(),
}

_type_registry = None


def get_type_reg():
    global _type_registry
    if not _type_registry:
        _type_registry = TypeRegistry()
        load_type_specs(_type_registry, get_session().spec_dir)

    return _type_registry


@create("type-registry")
def create_type_registry(term):
    global _type_registry
    if _type_registry:
        raise Exception("The type registry should be created only once")

    return get_type_reg()


@rule("project")
def created_project(project):
    return create_forward(project, has, ":type-registry")


@rule("type-registry")
def created_type_registry(type_reg):
    forwards = []
    for type_spec in get_type_reg().type_specs():
        if not type_spec.is_form:
            kebab_name = camel_to_kebab(l0(type_spec.type_name))
            forwards.append(create_forward(type_reg, has, f"{kebab_name}:item"))
            forwards.append(create_forward(type_reg, has, f"{kebab_name}:item~list"))
    return forwards


@extend(TypeRegistry)
class ExtendTypeReg:
    items = P.children(has, "item")
    item_lists = P.children(has, "item~list")
