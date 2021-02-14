from dataclasses import dataclass, field

from leapreact.component import Component
from leaptools.tool import Tool


@dataclass
class Module(Tool):
    name: str
    components: [Component] = field(default_factory=list)
    template_dirs: [(str, str)] = field(default_factory=list)

    @property
    def import_path(self):
        return f"src/{self.name}"

    def add_template_dir(self, root_filename, location):
        new_template_dir = (root_filename, location)
        if new_template_dir not in self.template_dirs:
            self.template_dirs.append(new_template_dir)
