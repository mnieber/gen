from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Module(Resource):
    name: str
    name_snake: str
