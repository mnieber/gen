from moonleap_react_view.router_and_module.props import create_component_router_config


def create_router_configs(self):
    router_config = create_component_router_config(self, url="")
    result = [router_config]
    return result
