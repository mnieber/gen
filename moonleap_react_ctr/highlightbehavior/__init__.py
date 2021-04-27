from moonleap import Prop, create_forward, extend, rule, tags
from moonleap.verbs import has, with_

from . import props
from .resources import HighlightBehavior


@tags(["highlight:behavior"])
def create_behavior(term, block):
    behavior = HighlightBehavior(name=term.data)
    return behavior


@rule("container", has + with_, "highlight:behavior")
def container_has_highlight_behavior(container, highlight_behavior):
    highlight_behaviour_str = "highlight:behavior"
    return create_forward(container, has, highlight_behaviour_str)


@extend(HighlightBehavior)
class ExtendBehavior:
    callbacks_section = Prop(props.callbacks_section)
    policies_section = Prop(props.policies_section)
