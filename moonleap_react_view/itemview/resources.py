from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class ItemView(Component):
    item_name: str
