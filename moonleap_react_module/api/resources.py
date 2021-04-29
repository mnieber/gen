from dataclasses import dataclass, field

from moonleap_react.component import Component


@dataclass
class Api(Component):
    has_load_effects: bool = field(default=True, init=False, compare=False)
