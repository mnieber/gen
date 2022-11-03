from dataclasses import dataclass

from titan.react_pkg.component import Component


@dataclass
class SelectItemEffect(Component):
    item_name: str
