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
from moonleap.utils.case import upper0
from moonleap.verbs import has, uses

from . import props
from .resources import (
    ItemView,
    create_load_item_effect,
    create_select_item_effect,
    get_graphql_item_lists,
    get_graphql_items,
)


@tags(["item-view"])
def create_item_view(term, block):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{upper0(name)}View")
    return item_view


@rule("item-view")
def maybe_add_load_item_effect_to_item_view(item_view):
    if not get_graphql_items(item_view):
        if get_graphql_item_lists(item_view):
            select_item_effect = create_select_item_effect(
                item_view, item_view.get_route_params()
            )
            return create_forward(
                item_view,
                has,
                ":select-item-effect",
                obj_res=select_item_effect,
            )
        return

    load_item_effect = create_load_item_effect(item_view, item_view.get_route_params())
    return [
        create_forward(
            item_view.module.service.api_module,
            has,
            ":load-item-effect",
            obj_res=load_item_effect,
        ),
        create_forward(
            item_view,
            uses,
            ":load-item-effect",
            obj_res=load_item_effect,
        ),
    ]


@extend(ItemView)
class ExtendItemView:
    render = MemFun(render_templates(__file__))
    get_route_params = MemFun(props.get_route_params)
    create_router_configs = MemFun(props.create_router_configs)
    load_item_effect = P.child(uses, "load-item-effect")
    select_item_effect = P.child(uses, "select-item-effect")
