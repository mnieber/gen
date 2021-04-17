from moonleap import MemFun, extend, kebab_to_camel, render_templates, tags

from .resources import ItemView


@tags(["item-view"])
def create_item_view(term, block):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{name}View")
    return item_view


@extend(ItemView)
class ExtendItemView:
    render = MemFun(render_templates(__file__))
