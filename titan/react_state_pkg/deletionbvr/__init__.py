from moonleap import Prop, create, extend, kebab_to_camel

from . import props
from .resources import DeletionBvr

base_tags = [("deletion", ["behavior"])]


@create("deletion")
def create_behavior(term, block):
    item_name = kebab_to_camel(term.data)
    behavior = DeletionBvr(item_name=item_name, name=term.tag)
    return behavior


@extend(DeletionBvr)
class ExtendDeletionBvr:
    sections = Prop(props.Sections)
