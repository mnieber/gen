from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.router.resources import prepend_router_configs
from titan.react_pkg.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_config = create_component_router_config(self)
    router_config.url = get_component_base_url(self, self.item_name)
    result = (
        prepend_router_configs(
            self.load_items_effect.create_router_configs(), [router_config]
        )
        if self.load_items_effect
        else [router_config]
    )

    for state in self.module.states:
        item_names = [x.item_name for x in state.item_lists]
        if state.state_provider and self.item_name in item_names:
            result = prepend_router_configs(
                state.state_provider.create_router_configs(), result
            )

    return result
