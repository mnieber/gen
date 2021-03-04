from dataclasses import dataclass

from moonleap_tools.tool import Tool


@dataclass
class Module(Tool):
    name: str
