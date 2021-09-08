import typing as T
from dataclasses import dataclass

from moonleap import Resource
from moonleap.resources.type_spec_store import TypeSpec


@dataclass
class Mutation(Resource):
    name: str
