from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class StateProvider(Component):
    item_name: str
