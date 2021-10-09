from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class ItemList(Resource):
    item_name: str
