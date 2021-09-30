from pathlib import Path

from moonleap import MemFun, create, extend, kebab_to_camel
from moonleap.utils.case import u0

from . import props
from .resources import ItemView

base_tags = [("item-view", ["component"])]


@create("item-view")
def create_item_view(term, block):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{u0(name)}View")
    item_view.add_template_dir(Path(__file__).parent / "templates")
    return item_view


@extend(ItemView)
class ExtendItemView:
    create_router_configs = MemFun(props.create_router_configs)
    get_chain = MemFun(props.get_chain)
