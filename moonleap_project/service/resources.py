from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Service(Resource):
    name: str
    use_default_config: bool
    shell: str = "sh"
    port: str = "80"
