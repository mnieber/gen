from dataclasses import dataclass

from moonleap import Resource


@dataclass
class RouteTable(Resource):
    import_path: str
    name: str
