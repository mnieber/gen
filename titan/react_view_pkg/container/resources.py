from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Container(Resource):
    name: str
