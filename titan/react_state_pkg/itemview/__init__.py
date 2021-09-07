import moonleap.resource.props as P
from moonleap import (
    MemFun,
    RenderTemplates,
    create_forward,
    extend,
    kebab_to_camel,
    rule,
    tags,
)
from moonleap.utils.case import upper0
from moonleap.verbs import has, uses

from . import props
from .resources import ItemView, create_load_item_effect, create_select_item_effect


@tags(["item-view"])
def create_item_view(term, block):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{upper0(name)}View")
    return item_view


@rule("item-view")
def maybe_add_load_item_effect_to_item_view(item_view):
    graphql_api = item_view.module.react_app.api_module.graphql_api
    item_queries = graphql_api.queries_that_provide_item(item_view.item_name)
    item_list_queries = graphql_api.queries_that_provide_item_list(item_view.item_name)

    if item_queries:
        load_item_effect = create_load_item_effect(
            item_view, item_view._get_route_params()
        )
        return [
            create_forward(
                item_view.module.react_app.api_module,
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

    # else if it loads item lists of this item type
    elif item_list_queries:
        select_item_effect = create_select_item_effect(
            item_view, item_view._get_route_params()
        )
        return create_forward(
            item_view,
            uses,
            ":select-item-effect",
            obj_res=select_item_effect,
        )


@extend(ItemView)
class ExtendItemView(RenderTemplates(__file__)):
    _get_route_params = MemFun(props._get_route_params)
    create_router_configs = MemFun(props.create_router_configs)
    load_item_effect = P.child(uses, "load-item-effect")
    select_item_effect = P.child(uses, "select-item-effect")
