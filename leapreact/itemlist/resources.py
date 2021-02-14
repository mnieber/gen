from dataclasses import dataclass

from moonleap import Resource


@dataclass
class ItemList(Resource):
    name: str
