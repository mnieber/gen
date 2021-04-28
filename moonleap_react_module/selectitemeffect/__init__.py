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
from moonleap.verbs import has, supports
from moonleap_react.module import Module

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
    item_name = kebab_to_camel(behavior.term.data) or state.item_name
    module = state.module
    if not [x for x in module.select_item_effects if x.item_name == item_name]:
        return create_forward(module, has, Term(item_name, "select-item-effect"))


@extend(SelectItemEffect)
class ExtendSelectItemEffect:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)


@extend(Module)
class ExtendModule:
    select_item_effects = P.children(has, "select-item-effect")
