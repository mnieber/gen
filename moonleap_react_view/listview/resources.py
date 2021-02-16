from dataclasses import dataclass

from moonleap.utils.inflect import plural
from moonleap_react.component import Component


@dataclass
class ListView(Component):
    item_name: str
