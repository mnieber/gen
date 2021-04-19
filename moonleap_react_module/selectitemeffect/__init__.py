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
    title0,
)
from moonleap.utils.inflect import singular
from moonleap.verbs import has
from moonleap_behaviors.container.resources import Container

from . import props
from .resources import SelectItemEffect


@tags(["select-item-effect"])
def create_select_item_effect(term, block):
    item_name = kebab_to_camel(term.data)
    name = f"Select{title0(item_name)}Effect"
    select_item_effect = SelectItemEffect(item_name=item_name, name=name)
    return select_item_effect


@rule("container", has, "selection:behavior")
def container_has_selection_behavior(container, behavior):
    item_name = singular(container.name)
    return create_forward(container, has, Term(item_name, "select-item-effect"))


@extend(SelectItemEffect)
class ExtendSelectItemEffect:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)


@extend(Container)
class ExtendContainer:
    select_item_effect = P.child(has, "select-item-effect")
