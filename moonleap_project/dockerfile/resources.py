import typing as T
from dataclasses import dataclass, field

from moonleap_tools.tool import Tool


@dataclass
class Dockerfile(Tool):
    is_dev: bool = False
    image_name: T.Optional[str] = None
    custom_steps: str = ""
    custom_steps_dev: str = ""
    env_vars: T.List[str] = field(default_factory=lambda: [])
    env_vars_dev: T.List[str] = field(default_factory=lambda: [])

    @property
    def name(self):
        return "Dockerfile" + (".dev" if self.is_dev else "")


@dataclass
class DockerImage(Tool):
    name: T.Optional[str] = None
    install_command: str = "apt-get update && apt-get install -y"
    pip: str = "pip3"
