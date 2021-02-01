from dataclasses import dataclass, field

from leapreact.component import Component
from leaptools.tool import Tool


@dataclass
class Module(Tool):
    name: str
    components: [Component] = field(default_factory=list)

    @property
    def import_path(self):
        return f"src/{self.name}"
