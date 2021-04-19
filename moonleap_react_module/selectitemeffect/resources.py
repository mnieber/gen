import typing as T
from dataclasses import dataclass, field

from moonleap_react.component import Component


@dataclass
class SelectItemEffect(Component):
    item_name: str
