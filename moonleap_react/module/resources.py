from dataclasses import dataclass, field

from moonleap_tools.tool import Tool


@dataclass
class Module(Tool):
    name: str

    @property
    def import_path(self):
        return f"src/{self.name}"
