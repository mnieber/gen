from pathlib import Path

from moonleap import MemFun, create, extend, kebab_to_camel, named
from moonleap.utils.case import u0

from . import props
from .resources import ItemView, NamedItemView

base_tags = [("item-view", ["component"])]


@create("item-view")
def create_item_view(term, block):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{u0(name)}View")
    item_view.add_template_dir(Path(__file__).parent / "templates", props.get_context)
    return item_view


@create("x+item-view")
def create_named_item_view(term, block):
    return NamedItemView()


@extend(ItemView)
class ExtendItemView:
    get_chain = MemFun(props.get_chain)
    create_router_configs = MemFun(props.create_router_configs)
