import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, extend, kebab_to_camel, render_templates, tags
from moonleap.verbs import has
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import State


@tags(["state"])
def create_state(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    state = State(name=name)
    add(state, load_node_package_config(__file__))
    return state


@extend(State)
class ExtendState:
    render = MemFun(render_templates(__file__))
    behaviors = P.children(has, "behavior")
    bvrs_by_item_name = Prop(props.bvrs_by_item_name)
    declare_policies_section = MemFun(props.declare_policies_section)
    policies_section = Prop(props.policies_section)
    constructor_section = Prop(props.constructor_section)
    callbacks_section = Prop(props.callbacks_section)
    type_import_path = MemFun(props.type_import_path)


@extend(Module)
class ExtendModule:
    state = P.child(has, "state")
