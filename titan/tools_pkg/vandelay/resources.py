from dataclasses import dataclass

from titan.project_pkg.service import Tool


@dataclass
class Vandelay(Tool):
    type: str
