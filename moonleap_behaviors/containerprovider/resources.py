from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class ContainerProvider(Component):
    item_name: str
