from dataclasses import dataclass

from titan.react_pkg.component.resources import Component


@dataclass
class StateProvider(Component):
    base_name: str
