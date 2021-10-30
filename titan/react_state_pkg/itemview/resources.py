from dataclasses import dataclass

from moonleap.resource.named_class import named
from titan.react_pkg.component import Component


@dataclass
class ItemView(Component):
    item_name: str

    def get_title(self):
        return u0(self.item_name)


NamedItemView = named(ItemView, base_klass=named(Component))
