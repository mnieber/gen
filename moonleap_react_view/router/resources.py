from dataclasses import dataclass

from moonleap import Resource
from moonleap_react.component import Component


class Router(Component):
    pass


@dataclass
class RouterConfig(Resource):
    url: str
    component_name: str
    module_name: str
    wraps: bool = False
