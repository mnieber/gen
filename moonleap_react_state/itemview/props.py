from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_config = create_component_router_config(self)
    router_config.url = f"{self.item_name}"
    result = [router_config]

    for select_item_effect in self.module.select_item_effects:
        result = prepend_router_configs(
            select_item_effect.create_router_configs(), result
        )

    return result
