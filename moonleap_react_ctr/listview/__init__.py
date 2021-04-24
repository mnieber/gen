import moonleap.resource.props as P
from moonleap import (
    MemFun,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
)
from moonleap.utils.inflect import plural
from moonleap.verbs import has, uses

from . import props
from .resources import ListView


@tags(["list-view"])
def create_list_view(term, block):
    name = kebab_to_camel(term.data)
    list_view = ListView(item_name=name, name=f"{name}ListView")
    return list_view


@rule("list-view", has, "behavior")
def list_view_uses_container(list_view, behavior):
    items_str = plural(list_view.item_name)
    container_term_str = f"{items_str}:container"
    return [
        create_forward(list_view, uses, container_term_str),
        create_forward(container_term_str, has, behavior),
    ]


@extend(ListView)
class ExtendListView:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
    container = P.child(uses, "container")
