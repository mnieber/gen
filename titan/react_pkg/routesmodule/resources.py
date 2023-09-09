from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Route(Resource):
    name: str
    path: str


@dataclass
class NavPage(Resource):
    pass
