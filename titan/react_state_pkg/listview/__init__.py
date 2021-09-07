from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
from moonleap.utils.case import upper0
from moonleap.utils.inflect import plural
from moonleap.verbs import has, uses
from titan.react_module_pkg.loaditemseffect import create_load_items_effect

from . import props
from .context import get_context
from .resources import ListView


@create("list-view", ["component"])
def create_list_view(term, block):
    name = kebab_to_camel(term.data)
    list_view = ListView(
        item_name=name, items_name=plural(name), name=f"{upper0(name)}ListView"
    )
    list_view.add_template_dir(Path(__file__).parent / "templates", get_context)
    return list_view


rules = [(("list-view", has, "behavior"), empty_rule())]


@extend(ListView)
class ExtendListView:
    create_router_configs = MemFun(props.create_router_configs)
    load_items_effect = P.child(uses, "load-items-effect")
    behaviors = P.children(has, "behavior")
