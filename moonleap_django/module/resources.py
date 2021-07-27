from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Module(Resource):
    name_snake: str
    name_camel: str
