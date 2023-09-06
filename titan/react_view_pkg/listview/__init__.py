from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import (
    create,
    create_forward,
    empty_rule,
    extend,
    parts_to_camel,
    rule,
    u0,
)
from moonleap.blocks.verbs import shows

from .resources import ListView

base_tags = {
    "list-view": ["component", "react-view"],
}

rules = {
    ("list-view", shows, "item~list"): empty_rule(),
}


@rule("x+list-view", shows, "item~list")
def named_list_view_show_item_list(named_list_view, item_list):
    return create_forward(named_list_view.typ, shows, item_list)


@create("list-view")
def create_list_view(term):
    name = u0(parts_to_camel(term.parts))
    view = ListView(name=f"{name}")
    view.template_dir = Path(__file__).parent / "templates"
    return view


@extend(ListView)
class ExtendListView:
    item_list = P.children(shows, "item~list")
