from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class Service(Resource):
    name: str
    shell: str = "sh"
    port: str = "80"
