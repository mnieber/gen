from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class Frame(Component):
    item_name: str
