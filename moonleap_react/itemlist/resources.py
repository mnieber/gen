from dataclasses import dataclass

from moonleap import Resource
from moonleap.utils.inflect import plural


@dataclass
class ItemList(Resource):
    name: str

    @property
    def plural_name(self):
        return plural(self.name)
