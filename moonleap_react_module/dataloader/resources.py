import typing as T
from dataclasses import dataclass, field

from moonleap_react.component import Component


@dataclass
class DataLoader(Component):
    pass
    # item_name: T.Optional[str] = field(default=None, init=False)
