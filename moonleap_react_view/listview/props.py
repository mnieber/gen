from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_configs = create_component_router_config(self)
    result = [router_configs]

    container = self.module.container
    container_provider = container.container_provider if container else None
    if container_provider:
        result = prepend_router_configs(
            container_provider.create_router_configs(), result
        )

    return result
