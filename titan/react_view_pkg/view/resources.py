from dataclasses import dataclass

from titan.react_pkg.component import Component


@dataclass
class View(Component):
    root_filename: str = __file__
    templates_dir: str = "templates"
