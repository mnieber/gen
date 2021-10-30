from dataclasses import dataclass

from moonleap import named
from titan.react_pkg.component import Component


@dataclass
class View(Component):
    wraps_children: bool = False
