import moonleap.packages.extensions.props as P
from moonleap import (
    Priorities,
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
)
from moonleap.blocks.verbs import has, stores
from titan.react_view_pkg.behavior.resources import Behavior
from titan.react_view_pkg.state.resources import State
from titan.types_pkg.itemlist import ItemList

from . import props
from .resources import Container

base_tags = {}


@create("container")
def create_container(term):
    name = kebab_to_camel(term.data)
    return Container(name=name)


@extend(State)
class ExtendState:
    containers = P.children(has, "container")


@extend(Container)
class ExtendContainer:
    state = P.parent("state", has)
    item_list = P.child(has + stores, "item~list")
    item = P.child(has + stores, "item")
    bvrs = P.children(has, "bvr")
    item_name = Prop(props.container_item_name)


@extend(Behavior)
class ExtendBehavior:
    container = P.parent("container", has)


@extend(ItemList)
class ExtendItemList:
    addition = P.child(has, "addition:bvr")


rules = {
    "container": {
        (has, "addition:bvr", Priorities.LOW.value): (
            #
            lambda container, addition_bvr: create_forward(
                container.item_list, has, addition_bvr
            )
        ),
        (has + stores, "item~list"): empty_rule(),
        (has + stores, "item"): empty_rule(),
        (has, "bvr"): empty_rule(),
    },
    "state": {(has, "container"): empty_rule()},
    "item~list": {(has, "bvr"): empty_rule()},
}
