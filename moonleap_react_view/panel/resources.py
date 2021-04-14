from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class Panel(Component):
    type: str
