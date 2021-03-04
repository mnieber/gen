from dataclasses import dataclass

from moonleap_react.component import Component


@dataclass
class View(Component):
    kebab_name: str
