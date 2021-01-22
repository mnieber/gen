from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Service(Resource):
    name: str
    shell: str = "sh"
