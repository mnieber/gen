from moonleap_react_view.router import RouterConfig
from moonleap_react_view.router.resources import reduce_router_configs


def create_router_configs(self):
    result = reduce_router_configs([RouterConfig(component=self, url="", wraps=True)])
    return result
