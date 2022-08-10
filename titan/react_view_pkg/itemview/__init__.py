from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, empty_rule, extend, kebab_to_camel, rule
from moonleap.utils.case import u0
from moonleap.verbs import uses

from .resources import ItemView, NamedItemView

base_tags = [("item-view", ["component"])]

rules = [(("item-view", uses, "item"), empty_rule())]


@create("item-view")
def create_item_view(term):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{u0(name)}View")
    item_view.template_dir = Path(__file__).parent / "templates"
    return item_view


@rule("item-view")
def item_view_created(item_view):
    return create_forward(item_view, uses, f"{item_view.meta.term.data}:item")


@create("x+item-view")
def create_named_item_view(term):
    return NamedItemView()


@extend(ItemView)
class ExtendItemView:
    item = P.child(uses, "item", required=True)
