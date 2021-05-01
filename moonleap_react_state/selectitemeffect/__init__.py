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
from moonleap.verbs import has, provides
from moonleap_react.module import Module

from . import props
from .resources import SelectItemEffect


@tags(["select-item-effect"])
def create_select_item_effect(term, block):
    item_name = kebab_to_camel(term.data)
    name = f"Select{upper0(item_name)}Effect"
    select_item_effect = SelectItemEffect(item_name=item_name, name=name)
    return select_item_effect


@rule("state", provides, "selection")
def state_provides_selection(state, selectionbvr):
    return create_forward(
        state.module, has, Term(selectionbvr.item_name, "select-item-effect")
    )


@extend(SelectItemEffect)
class ExtendSelectItemEffect:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)


@extend(Module)
class ExtendModule:
    select_item_effects = P.children(has, "select-item-effect")
