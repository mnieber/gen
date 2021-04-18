from moonleap import create_forward, rule
from moonleap.resource.rel import Forwards
from moonleap.verbs import has, loads


@rule("graphql:api", loads, "item")
def graphqlapi_loads_item(graphql_api, item):
    dataloader_term_str = f"{item.name}:dataloader"
    return Forwards(
        [
            create_forward(graphql_api.module, has, dataloader_term_str),
            create_forward(dataloader_term_str, loads, item),
        ]
    )


@rule("graphql:api", loads, "item-list")
def graphqlapi_loads_item_list(graphql_api, item_list):
    dataloader_term_str = f"{item_list.item_name}-list:dataloader"
    return Forwards(
        [
            create_forward(graphql_api.module, has, dataloader_term_str),
            create_forward(dataloader_term_str, loads, item_list),
        ]
    )
