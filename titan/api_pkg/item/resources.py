from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Item(Resource):
    item_name: str
    item_name_snake: str
