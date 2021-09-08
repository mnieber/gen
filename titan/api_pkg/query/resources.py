import typing as T
from dataclasses import dataclass, field

from moonleap import Resource
from moonleap.resources.data_type_spec_store import DataTypeSpec


@dataclass
class Query(Resource):
    name: str
    fields: T.List[str] = field(default_factory=list)
    data_type_in: T.Optional[DataTypeSpec] = None
