from dataclasses import dataclass

from moonleap import Resource


@dataclass
class ReactModule(Resource):
    name: str
