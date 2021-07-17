from dataclasses import dataclass, field

from moonleap_react.component import Component


@dataclass
class GraphqlApi(Component):
    has_load_effects: bool = field(default=True, init=False, compare=False)


def get_graphql_item_lists(api_module, item_name):
    if not api_module.graphql_api:
        return

    return [
        x for x in api_module.graphql_api.item_lists_loaded if x.item_name == item_name
    ]


def get_graphql_items(api_module, item_name):
    if not api_module.graphql_api:
        return

    return [x for x in api_module.graphql_api.items_loaded if x.item_name == item_name]
