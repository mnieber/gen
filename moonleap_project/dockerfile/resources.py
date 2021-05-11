from dataclasses import dataclass, field

from moonleap_tools.tool import Tool


@dataclass
class Dockerfile(Tool):
    is_dev: bool = False
    image_name: str = None
    env_vars: [str] = field(default_factory=lambda: [])
    env_vars_dev: [str] = field(default_factory=lambda: [])

    @property
    def name(self):
        return "Dockerfile" + (".dev" if self.is_dev else "")


@dataclass
class DockerImage(Tool):
    name: str = None
    install_command: str = "apt-get update && apt-get install -y"
    pip: str = "pip3"
