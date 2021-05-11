from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class Service(Resource):
    name: str
    use_default_config: bool
    shell: str = "sh"
    port: str = "80"
    install_dir: str = "/app"
    env_files: [str] = field(default_factory=lambda: [])
    env_files_dev: [str] = field(default_factory=lambda: [])
