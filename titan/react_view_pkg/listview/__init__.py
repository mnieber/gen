from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, empty_rule, extend, kebab_to_camel, rule
from moonleap.utils.case import u0
from moonleap.utils.inflect import plural
from moonleap.verbs import has, uses
from titan.react_view_pkg.listviewitem.resources import ListViewItem

from .resources import ListView

base_tags = {"list-view": ["component"]}

rules = {
    ("list-view", uses, "item"): empty_rule(),
    ("list-view", uses, "lvi"): empty_rule(),
    ("list-view", has, "behavior"): empty_rule(),
}


@create("list-view")
def create_list_view(term):
    name = kebab_to_camel(term.data)
    list_view = ListView(
        item_name=name, items_name=plural(name), name=f"{u0(name)}ListView"
    )
    list_view.template_dir = Path(__file__).parent / "templates"
    return list_view


@rule("list-view")
def created_list_view(list_view):
    return [
        create_forward(list_view, uses, f"{list_view.meta.term.data}:item"),
        create_forward(list_view, uses, f"{list_view.meta.term.data}:lvi"),
    ]


@extend(ListView)
class ExtendListView:
    bvrs = P.children(has, "behavior")
    item = P.child(uses, "item", required=True)
    lvi = P.child(uses, "lvi", required=True)


@extend(ListViewItem)
class ExtendListViewItem:
    list_view = P.parent("list-view", uses, required=True)
