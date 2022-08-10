import typing as T
from dataclasses import dataclass

from titan.project_pkg.service import Tool


@dataclass
class Dockerfile(Tool):
    target: str
    image_name: T.Optional[str] = None


@dataclass
class DockerImage(Tool):
    name: T.Optional[str] = None

    @property
    def install_command(self):
        if self.name and self.name.startswith("node:"):
            return "apk update && apk add"
        return "apt-get update && apt-get install -y"
