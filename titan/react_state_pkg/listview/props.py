from moonleap.utils.inflect import plural
from titan.api_pkg.typeregistry import TypeRegistry
from titan.react_pkg.component.props import create_router_configs_from_chain
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.pkg.get_chain import get_chain_to
from titan.react_pkg.pkg.ml_get import ml_graphql_api, ml_react_app
from titan.react_pkg.router_and_module.props import create_component_router_config


def create_router_configs(self):
    result = create_router_configs_from_chain(self.get_chain() or [])
    url = get_component_base_url(self, plural(self.item_name))
    router_config = create_component_router_config(self, url=url)
    result.append(router_config)

    return result


def get_chain(self):
    graphql_api = ml_graphql_api(ml_react_app(self))
    type_reg = TypeRegistry(graphql_api)
    return get_chain_to(type_reg.get_item_list_by_name(self.item_name))
