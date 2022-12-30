from dataclasses import dataclass

from moonleap import Resource, u0
from moonleap.utils.inflect import plural


@dataclass
class Behavior(Resource):
    name: str
    item_name: str
    has_param: bool

    @property
    def items_name(self):
        return plural(self.item_name)

    @property
    def ts_var(self):
        return self.item_name + u0(self.name)
