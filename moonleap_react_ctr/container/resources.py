from dataclasses import dataclass

from moonleap.utils.inflect import singular
from moonleap_react.component import Component


@dataclass
class Container(Component):
    @property
    def item_name(self):
        return singular(self.name)
