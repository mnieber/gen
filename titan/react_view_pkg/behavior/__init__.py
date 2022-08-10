import moonleap.resource.props as P
from moonleap import create, create_forward, empty_rule, extend, named, rule
from moonleap.verbs import has
from titan.api_pkg.itemlist.resources import ItemList

from .resources import Behavior

base_tags = [
    ("highlight", ["behavior"]),
    ("selection", ["behavior"]),
    ("filtering", ["behavior"]),
    ("deletion", ["behavior"]),
]

rules = [
    (("x+item~list", has, "behavior"), empty_rule()),
]


@create("behavior")
def create_behavior(term):
    return Behavior(item_name=term.data, name=term.tag)


@rule("x+item~list", has, "selection")
def named_item_list_has_selection(named_item_list, selection):
    named_item_list.pipeline.state.module.react_app.get_module("utils").use_packages(
        ["mergeClickHandlers"]
    )
    return create_forward(named_item_list, has, f"{selection.meta.term.data}:highlight")


@extend(named(ItemList))
class ExtendNamedItemList:
    bvrs = P.children(has, "behavior")
