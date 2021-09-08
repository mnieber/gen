from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Query(Resource):
    name: str
