from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class Service(Resource):
    name: str
    shell: str = "sh"
    template_dirs: [(str, str)] = field(default_factory=list)

    def add_template_dir(self, root_filename, location):
        new_template_dir = (root_filename, location)
        if new_template_dir not in self.template_dirs:
            self.template_dirs.append(new_template_dir)
