import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Term,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    upper0,
)
from moonleap.utils.inflect import singular
from moonleap.verbs import has, supports
from moonleap_react_state.state.resources import State

from . import props
from .resources import SelectItemEffect


@tags(["select-item-effect"])
def create_select_item_effect(term, block):
    item_name = kebab_to_camel(term.data)
    name = f"Select{upper0(item_name)}Effect"
    select_item_effect = SelectItemEffect(item_name=item_name, name=name)
    return select_item_effect


@rule("state", supports, "selection")
def state_has_selection_behavior(state, behavior):
    item_name = singular(state.name)
    return create_forward(state, has, Term(item_name, "select-item-effect"))


@extend(SelectItemEffect)
class ExtendSelectItemEffect:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)


@extend(State)
class ExtendState:
    select_item_effect = P.child(has, "select-item-effect")
