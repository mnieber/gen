from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Mutation(Resource):
    name: str
