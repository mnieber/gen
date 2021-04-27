from moonleap import Prop, create_forward, extend, rule, tags
from moonleap.verbs import has, with_

from . import props
from .resources import SelectionBehavior


@tags(["selection:behavior"])
def create_behavior(term, block):
    behavior = SelectionBehavior(name=term.data)
    return behavior


@rule("container", has + with_, "selection:behavior")
def container_has_selection_behavior(container, selection_behavior):
    highlight_behaviour_str = "highlight:behavior"
    return create_forward(container, has, highlight_behaviour_str)


@extend(SelectionBehavior)
class ExtendBehavior:
    imports_section = Prop(props.imports_section)
    callbacks_section = Prop(props.callbacks_section)
    declare_policies_section = Prop(props.declare_policies_section)
    policies_section = Prop(props.policies_section)
