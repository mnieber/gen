import typing as T
from dataclasses import dataclass

from moonleap_project.service import Tool


@dataclass
class Dockerfile(Tool):
    is_dev: bool = False
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
