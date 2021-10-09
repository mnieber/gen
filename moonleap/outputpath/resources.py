from dataclasses import dataclass

from moonleap.resource import Resource


@dataclass
class OutputPath(Resource):
    location: str
