from dataclasses import dataclass
from moonleap import Resource


@dataclass
class Project(Resource):
    name: str
