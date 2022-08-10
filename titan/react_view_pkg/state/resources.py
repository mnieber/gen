from dataclasses import dataclass

from moonleap.utils.inflect import singular
from titan.react_pkg.component import Component


@dataclass
class State(Component):
    @property
    def item_name(self):
        return singular(self.name)
