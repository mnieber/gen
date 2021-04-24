from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class LoadItemsEffect(Component):
    item_name: str
