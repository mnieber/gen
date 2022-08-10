from dataclasses import dataclass

from moonleap import Resource
from titan.react_pkg.component import Component


class Router(Component):
    pass


@dataclass
class RouteTable(Resource):
    import_path: str
    name: str
