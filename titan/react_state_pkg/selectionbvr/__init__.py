from moonleap import Prop, create, create_forward, extend, kebab_to_camel, rule
from moonleap.verbs import has

from . import props
from .resources import SelectionBvr

base_tags = [("selection", ["behavior"])]


@create("selection")
def create_behavior(term, block):
    item_name = kebab_to_camel(term.data)
    behavior = SelectionBvr(item_name=item_name, name=term.tag)
    return behavior


@rule("x+item~list", has, "selection")
def named_item_list_has_selection(named_item_list, selection):
    named_item_list.pipeline.state.module.react_app.utils_module.use_packages(
        ["mergeClickHandlers"]
    )
    return create_forward(named_item_list, has, f"{selection.item_name}:highlight")


@extend(SelectionBvr)
class ExtendSelectionBvr:
    sections = Prop(props.Sections)
