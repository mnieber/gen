from dataclasses import dataclass

from moonleap import Resource


@dataclass
class ItemType(Resource):
    name: str
    name_snake: str
