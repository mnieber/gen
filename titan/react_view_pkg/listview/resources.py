from dataclasses import dataclass

from moonleap import u0
from titan.react_pkg.component import Component


@dataclass
class ListView(Component):
    item_name: str
    items_name: str

    def get_title(self):
        return u0(self.items_name)
