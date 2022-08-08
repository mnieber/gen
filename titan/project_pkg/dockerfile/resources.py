import typing as T
from dataclasses import dataclass

from titan.project_pkg.service import Tool


@dataclass
class Dockerfile(Tool):
    target: str
    image_name: T.Optional[str] = None
    custom_steps_pre: str = ""
    custom_steps_pre_dev: str = ""
    custom_steps: str = ""
    custom_steps_dev: str = ""


@dataclass
class DockerImage(Tool):
    name: T.Optional[str] = None
    install_command: str = "apt-get update && apt-get install -y"
    pip: str = "pip3"
