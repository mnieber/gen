from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_config = create_component_router_config(self)
    router_config.url = "view"
    result = [router_config]

    container = self.module.container

    select_item_effect = container.select_item_effect if container else None
    if select_item_effect:
        result = prepend_router_configs(
            select_item_effect.create_router_configs(), result
        )

    container_provider = container.container_provider if container else None
    if container_provider:
        result = prepend_router_configs(
            container_provider.create_router_configs(), result
        )

    return result
