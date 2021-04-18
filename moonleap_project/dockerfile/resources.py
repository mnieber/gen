from dataclasses import dataclass

from moonleap_tools.tool import Tool


@dataclass
class Dockerfile(Tool):
    is_dev: bool = False
    image_name: str = None

    @property
    def name(self):
        return "Dockerfile" + (".dev" if self.is_dev else "")


@dataclass
class DockerImage(Tool):
    name: str = None
    install_command: str = "apt-get update && apt-get install -y"
