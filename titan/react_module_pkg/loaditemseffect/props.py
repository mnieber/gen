from titan.react_view_pkg.router_and_module.props import create_component_router_config


def create_router_configs(self):
    return [create_component_router_config(self, url="")]
