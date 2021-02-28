from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class Store(Component):
    @property
    def useRST(self):
        return True
