from dataclasses import dataclass

from moonleap_tools.tool import Tool
from moonleap import Resource


@dataclass
class Dockerfile(Resource):
    is_dev: bool = False
    install_command: str = "apt-get update && apt-get install -y"
    image_name: str = None

    @property
    def name(self):
        return "Dockerfile" + (".dev" if self.is_dev else "")


@dataclass
class DockerImage(Tool):
    name: str = None
