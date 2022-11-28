from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Config(Resource):
    name: str
