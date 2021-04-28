from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_configs = create_component_router_config(self)
    result = [router_configs]

    state = self.module.state
    state_provider = state.state_provider if state else None
    if state_provider:
        result = prepend_router_configs(state_provider.create_router_configs(), result)

    return result