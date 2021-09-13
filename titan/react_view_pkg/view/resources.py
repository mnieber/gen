from dataclasses import dataclass
from pathlib import Path

from titan.react_pkg.component import Component


@dataclass
class View(Component):
    templates_dir: str = str(Path(__file__).parent / "templates")
