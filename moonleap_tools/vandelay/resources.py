from dataclasses import dataclass

from moonleap_project.service import Tool


@dataclass
class Vandelay(Tool):
    type: str
