import typing as T
from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Mutation(Resource):
    name: str
    data_type_inputs: T.Any = None
