from moonleap import MemFun, extend, tags

from . import props
from .resources import HighlightBvr


@tags(["highlight"])
def create_behavior(term, block):
    behavior = HighlightBvr(name=term.tag)
    return behavior


@extend(HighlightBvr)
class ExtendHighlightBvr:
    callbacks_section = MemFun(props.callbacks_section)
    policies_section = MemFun(props.policies_section)
    default_props_section = MemFun(props.default_props_section)
