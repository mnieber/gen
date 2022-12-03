from dataclasses import dataclass

from titan.react_pkg.component import Component


@dataclass
class ListView(Component):
    item_name: str
    items_name: str
