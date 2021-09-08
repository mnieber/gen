import typing as T
from dataclasses import dataclass

from moonleap import Resource
from moonleap.resources.data_type_spec_store import DataTypeSpec


@dataclass
class Mutation(Resource):
    name: str
    data_type_in: T.Optional[DataTypeSpec] = None
