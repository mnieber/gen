from dataclasses import dataclass

from moonleap import Resource
from moonleap_react.component import Component


class Router(Component):
    pass


@dataclass
class RouterConfig(Resource):
    component: Component
    wraps: bool = False
