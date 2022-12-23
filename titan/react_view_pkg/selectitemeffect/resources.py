from dataclasses import dataclass

from titan.react_pkg.component.resources import Component


@dataclass
class SelectItemEffect(Component):
    item_name: str
