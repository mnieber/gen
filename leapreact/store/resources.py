from dataclasses import dataclass

from leapreact.component import Component


@dataclass
class Store(Component):
    pass

    @property
    def useRST(self):
        return True
