from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Item(Resource):
    name: str
