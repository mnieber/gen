from moonleap import Prop, extend, tags

from . import props
from .resources import HighlightBvr


@tags(["highlight"])
def create_behavior(term, block):
    behavior = HighlightBvr(name=term.tag)
    return behavior


@extend(HighlightBvr)
class ExtendHighlightBvr:
    callbacks_section = Prop(props.callbacks_section)
    policies_section = Prop(props.policies_section)
