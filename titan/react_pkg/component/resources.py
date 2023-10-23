from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Component(Resource):
    name: str

    def __post_init__(self):
        self.builder = None
