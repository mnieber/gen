from dataclasses import dataclass

from titan.react_pkg.component import Component

base_tags = [("store", ["react-store"])]


@dataclass
class Store(Component):
    pass
