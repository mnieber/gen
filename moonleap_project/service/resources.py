import typing as T
from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class Service(Resource):
    name: str
    use_default_config: bool
    shell: str = "sh"
    port: T.Optional[str] = None
    install_dir: str = "/app"
    env_files: T.List[str] = field(default_factory=lambda: [])
    env_files_dev: T.List[str] = field(default_factory=lambda: [])


@dataclass
class Tool(Resource):
    name: str
