
import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend, parts_to_camel, u0
from moonleap.blocks.verbs import has, shows

from .resources import ListView

base_tags = {
    "list-view": ["component", "react-view"],
}


@create("list-view")
def create_list_view(term):
    name = u0(parts_to_camel(term.parts))
    view = ListView(name=f"{name}")
    return view


@extend(ListView)
class ExtendListView:
    item_list = P.child(shows, "item~list")
    key_handler = P.child(has, "key-handler")
    selection_bvr = P.child(has, "selection:bvr")
    highlight_bvr = P.child(has, "highlight:bvr")
    drag_and_drop_bvr = P.child(has, "drag-and-drop:bvr")


rules = {
    "list-view": {
        (shows, "item~list"): empty_rule(),
        (has, "bvr"): empty_rule(),
        (has, "key-handler"): empty_rule(),
    },
}
