import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, extend, kebab_to_camel, render_templates, tags
from moonleap.verbs import has, provides
from titan.react_pkg.module import Module
from titan.react_pkg.nodepackage import load_node_package_config

from . import props
from .resources import State


@tags(["state"])
def create_state(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    state = State(name=name)
    add(state, load_node_package_config(__file__))
    return state


@extend(Module)
class ExtendModule:
    states = P.children(has, "state")


@extend(State)
class ExtendState:
    render = MemFun(render_templates(__file__))

    behaviors = P.children(provides, "behavior")
    item_lists = P.children(provides, "item-list")
    items = P.children(provides, "item")
    bvrs_by_item_name = Prop(props.bvrs_by_item_name)
    store_by_item_name = Prop(props.store_by_item_name)

    p_section_constructor = Prop(props.p_section_constructor)
    p_section_callbacks = Prop(props.p_section_callbacks)
    p_section_policies = Prop(props.p_section_policies)
    p_section_declare_policies = MemFun(props.p_section_declare_policies)
    type_import_path = MemFun(props.type_import_path)
