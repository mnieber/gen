from dataclasses import dataclass

from moonleap.utils import title
from moonleap.utils.inflect import plural
from moonleap_react.component import Component


@dataclass
class ListView(Component):
    item_name: str

    @property
    def loader_name(self):
        return f"Load{plural(title(self.item_name))}Effect"
