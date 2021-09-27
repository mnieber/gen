from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, create, create_forward, extend, kebab_to_camel, rule
from moonleap.utils.case import upper0
from moonleap.verbs import has, uses
from titan.react_module_pkg.loaditemeffect.resources import create_name_postfix

from . import props
from .resources import ItemView


@create("item-view", ["component"])
def create_item_view(term, block):
    name = kebab_to_camel(term.data)
    item_view = ItemView(item_name=name, name=f"{upper0(name)}View")
    item_view.add_template_dir(Path(__file__).parent / "templates")
    return item_view


@rule("item-view", priority=5)
def maybe_add_load_item_effect_to_item_view(item_view):
    api_module = item_view.module.react_app.api_module
    graphql_api = api_module.graphql_api
    item_name_kebab = item_view._meta.term.data

    # if the graphql_api loads items of this item type
    if graphql_api.queries_that_provide_item(item_view.item_name):
        route_params = item_view._get_route_params()
        name_post_fix = create_name_postfix(item_view.item_name, route_params)
        load_item_effect_term_str = (
            f"load-{item_name_kebab}-by-{name_post_fix}:load-item-effect"
        )
        return [
            create_forward(api_module, has, load_item_effect_term_str),
            create_forward(item_view, uses, load_item_effect_term_str),
        ]

    # else if it loads item lists of this item type
    elif graphql_api.queries_that_provide_item_list(item_view.item_name):
        select_item_effect_term_str = f"select-{item_name_kebab}:select-item-effect"
        return create_forward(item_view, uses, select_item_effect_term_str)


@extend(ItemView)
class ExtendItemView:
    _get_route_params = MemFun(props._get_route_params)
    create_router_configs = MemFun(props.create_router_configs)
    load_item_effect = P.child(uses, "load-item-effect")
    select_item_effect = P.child(uses, "select-item-effect")
