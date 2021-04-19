from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class Picker(Component):
    item_name: str
