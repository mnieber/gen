import ramda as R
from moonleap import get_tweaks
from moonleap_react.component.resources import get_component_base_url
from moonleap_react_view.router.resources import prepend_router_configs
from moonleap_react_view.router_and_module.props import create_component_router_config


def _get_route_params(self):
    default_params = [] if self.load_item_effect else [f"{self.item_name}Id"]
    return R.path_or(
        default_params,
        ["services", self.module.service.name, "components", self.name, "route_params"],
    )(get_tweaks())


def create_router_configs(self):
    router_config = create_component_router_config(self)
    base_url = get_component_base_url(self, self.item_name)
    router_config.url = "/".join(
        ([base_url] if base_url else [])
        + [":" + x for x in _get_route_params(self) if x is not None]
    )
    result = [router_config]

    # Add router configs for load-item-effect
    if self.load_item_effect:
        result = prepend_router_configs(
            self.load_item_effect.create_router_configs(), result
        )

    if self.select_item_effect:
        result = prepend_router_configs(
            self.select_item_effect.create_router_configs(), result
        )

    # Add router configs for state-provider
    for submodule in self.module.service.modules:
        for state in submodule.states:
            item_names = (
                [x.item_name for x in state.items]
                if self.load_item_effect
                else [x.item_name for x in state.item_lists]
            )
            if state.state_provider and self.item_name in item_names:
                result = prepend_router_configs(
                    state.state_provider.create_router_configs(), result
                )

    return result
