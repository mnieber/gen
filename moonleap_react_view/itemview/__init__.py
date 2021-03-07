import moonleap.resource.props as P
from moonleap import (
    MemFun,
    add,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    title0,
)
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.module import Module
from moonleap_react_view.router import RouterConfig

from .resources import ItemView


@tags(["item-view"])
def create_item_view(term, block):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{name}View")
    return item_view


@rule("module", has, "item-view")
def add_items_view(module, item_view):
    add(
        item_view,
        RouterConfig(
            url=f"/{module.name}/:{item_view.item_name}Id/",
            component_name=title0(item_view.name),
            module_name=module.name,
        ),
    )
    return create_forward(module.service, has, "items:module")


@rule("module", has, "item-view")
def module_has_item_view(module, item_view):
    item_view.output_path = module.output_path
    return service_has_tool_rel(module.service, item_view)


@extend(ItemView)
class ExtendItemView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "item-view")
