from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class SelectItemEffect(Component):
    item_name: str
