from dataclasses import dataclass

from leaptools.tool import Tool


@dataclass
class Module(Tool):
    name: str

    @property
    def import_path(self):
        return f"src/{self.name}"
