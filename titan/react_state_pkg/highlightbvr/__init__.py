from moonleap import MemFun, extend, kebab_to_camel, tags

from . import props
from .resources import HighlightBvr


@tags(["highlight"])
def create_behavior(term, block):
    item_name = kebab_to_camel(term.data)
    behavior = HighlightBvr(item_name=item_name, name=term.tag)
    return behavior


@extend(HighlightBvr)
class ExtendHighlightBvr:
    p_section_callbacks = MemFun(props.p_section_callbacks)
    p_section_policies = MemFun(props.p_section_policies)
    p_section_default_props = MemFun(props.p_section_default_props)
