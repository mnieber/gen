from dataclasses import dataclass

from moonleap import Resource


@dataclass
class DodoLayerGroup(Resource):
    name: str
