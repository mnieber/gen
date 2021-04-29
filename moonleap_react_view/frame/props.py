from moonleap_react_view.router import RouterConfig
from moonleap_react_view.router.resources import (
    prepend_router_configs,
    reduce_router_configs,
)


def create_router_configs(self):
    result = reduce_router_configs([RouterConfig(component=self, url="", wraps=True)])

    if self.state_provider:
        result = prepend_router_configs(
            self.state_provider.create_router_configs(), result
        )

    return result
