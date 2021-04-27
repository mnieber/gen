from moonleap import Prop, create_forward, extend, rule, tags
from moonleap.verbs import supports

from . import props
from .resources import SelectionBvr


@tags(["selection"])
def create_behavior(term, block):
    behavior = SelectionBvr(item_name=term.data, name=term.tag)
    return behavior


@rule("container", supports, "selection")
def container_supports_selection(container, selection):
    return create_forward(container, supports, f"{selection.item_name}:highlight")


@extend(SelectionBvr)
class ExtendSelectionBvr:
    imports_section = Prop(props.imports_section)
    callbacks_section = Prop(props.callbacks_section)
    declare_policies_section = Prop(props.declare_policies_section)
    policies_section = Prop(props.policies_section)
