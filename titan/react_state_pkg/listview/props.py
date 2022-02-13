from moonleap.utils.inflect import plural
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)
from titan.react_view_pkg.pkg.create_router_configs_from_chain import (
    create_router_configs_from_chain,
)


def create_router_configs(self, named_component):
    result = create_router_configs_from_chain([])
    url = get_component_base_url(self, plural(self.item_name))
    router_config = create_component_router_config(
        self, named_component=named_component, url=url
    )
    result.append(router_config)

    return result
