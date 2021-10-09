from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class Item(Resource):
    item_name: str
