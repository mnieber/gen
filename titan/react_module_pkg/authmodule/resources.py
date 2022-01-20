from dataclasses import dataclass

from titan.react_pkg.component import Component
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)
from titan.react_view_pkg.view import View


@dataclass
class AuthStore(Component):
    pass


class AuthSwitchView(View):
    def create_router_configs(self, named_component):
        return [
            create_component_router_config(
                self, named_component=named_component, url=""
            )
        ]
