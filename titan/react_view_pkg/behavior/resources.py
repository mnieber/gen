from dataclasses import dataclass

from moonleap import Resource
from moonleap.utils.inflect import plural


@dataclass
class Behavior(Resource):
    name: str
    item_name: str
    has_param: bool

    @property
    def items_name(self):
        return plural(self.item_name)
