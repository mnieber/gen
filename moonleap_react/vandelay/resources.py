from dataclasses import dataclass

from moonleap_tools.tool import Tool


@dataclass
class Vandelay(Tool):
    type: str
