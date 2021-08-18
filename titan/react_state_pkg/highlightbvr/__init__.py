from moonleap import Prop, extend, kebab_to_camel, tags

from . import props
from .resources import HighlightBvr


@tags(["highlight"])
def create_behavior(term, block):
    item_name = kebab_to_camel(term.data)
    behavior = HighlightBvr(item_name=item_name, name=term.tag)
    return behavior


@extend(HighlightBvr)
class ExtendHighlightBvr:
    sections = Prop(props.Sections)
