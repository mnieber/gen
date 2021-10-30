from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)
from titan.react_view_pkg.view import View


class AuthSwitchView(View):
    def create_router_configs(self, named_component):
        return [
            create_component_router_config(
                self, named_component=named_component, url=""
            )
        ]
