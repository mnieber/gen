from moonleap.utils.inflect import plural
from titan.api_pkg.typeregistry import TypeRegistry
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.pkg.get_chain import get_chain_to
from titan.react_pkg.pkg.ml_get import ml_graphql_api, ml_react_app
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)
from titan.react_view_pkg.pkg.create_router_configs_from_chain import (
    create_router_configs_from_chain,
)


def create_router_configs(self, named_component):
    result = create_router_configs_from_chain(self.get_chain() or [])
    url = get_component_base_url(self, plural(self.item_name))
    router_config = create_component_router_config(
        self, named_component=named_component, url=url
    )
    result.append(router_config)

    return result


def get_chain(self):
    graphql_api = ml_graphql_api(ml_react_app(self))
    type_reg = TypeRegistry(graphql_api)
    return get_chain_to(type_reg.get_item_list_by_name(self.item_name))
