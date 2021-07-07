from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_configs = create_component_router_config(self)
    result = [router_configs]

    api_module = getattr(self.module.service, "api_module")
    if api_module:
        for load_items_effect in api_module.load_items_effects:
            if load_items_effect.item_name == self.item_name:
                result = prepend_router_configs(
                    load_items_effect.create_router_configs(), result
                )

    for state in self.module.states:
        item_names = [x.item_name for x in state.item_lists]
        if state.state_provider and self.item_name in item_names:
            result = prepend_router_configs(
                state.state_provider.create_router_configs(), result
            )

    return result
