from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Behavior(Resource):
    name: str
