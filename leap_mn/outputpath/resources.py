from dataclasses import dataclass

from moonleap import Resource


@dataclass
class OutputPath(Resource):
    location: str
