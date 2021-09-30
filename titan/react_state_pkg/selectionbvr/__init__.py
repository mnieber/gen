import moonleap.resource.props as P
from moonleap import Prop, create, create_forward, extend, kebab_to_camel, rule
from moonleap.verbs import provides
from titan.react_state_pkg.state.resources import State

from . import props
from .resources import SelectionBvr

base_tags = [("selection", ["behavior"])]


@create("selection")
def create_behavior(term, block):
    item_name = kebab_to_camel(term.data)
    behavior = SelectionBvr(item_name=item_name, name=term.tag)
    return behavior


@rule("state", provides, "selection")
def state_provides_selection(state, selection):
    return create_forward(state, provides, f"{selection.item_name}:highlight")


@extend(SelectionBvr)
class ExtendSelectionBvr:
    sections = Prop(props.Sections)


@extend(State)
class ExtendState:
    selections = P.children(provides, "selection")
