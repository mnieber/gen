from moonleap import Prop, add, create_forward, extend, rule, tags
from moonleap.verbs import has
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import SelectionBehavior


@tags(["selection:behavior"])
def create_behavior(term, block):
    behavior = SelectionBehavior(name=term.data)
    add(behavior, load_node_package_config(__file__))
    return behavior


@rule("container", has, "selection:behavior")
def container_has_selection_behavior(container, selection_behavior):
    highlight_behaviour_str = "highlight:behavior"
    return create_forward(container, has, highlight_behaviour_str)


@extend(SelectionBehavior)
class ExtendBehavior:
    imports_section = Prop(props.imports_section)
    callbacks_section = Prop(props.callbacks_section)
    declare_policies_section = Prop(props.declare_policies_section)
    policies_section = Prop(props.policies_section)
