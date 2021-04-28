from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_config = create_component_router_config(self)
    router_config.url = "view"
    result = [router_config]

    state = self.module.state

    select_item_effects = state.module.select_item_effects if state else None
    for select_item_effect in select_item_effects:
        result = prepend_router_configs(
            select_item_effect.create_router_configs(), result
        )

    state_provider = state.state_provider if state else None
    if state_provider:
        result = prepend_router_configs(state_provider.create_router_configs(), result)

    return result
