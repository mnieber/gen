from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class ListView(Component):
    item_name: str