from moonleap import MemFun, Prop, create_forward, extend, rule, tags
from moonleap.verbs import provides

from . import props
from .resources import SelectionBvr


@tags(["selection"])
def create_behavior(term, block):
    behavior = SelectionBvr(name=term.tag)
    return behavior


@rule("state", provides, "selection")
def state_provides_selection(state, selection):
    return create_forward(state, provides, f"{selection.item_name}:highlight")


@extend(SelectionBvr)
class ExtendSelectionBvr:
    imports_section = Prop(props.imports_section)
    callbacks_section = MemFun(props.callbacks_section)
    declare_policies_section = MemFun(props.declare_policies_section)
    policies_section = MemFun(props.policies_section)
    default_props_section = MemFun(props.default_props_section)
