import typing as T
from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class Query(Resource):
    name: str
    fields: T.List[str] = field(default_factory=list)
    data_type_inputs: T.Any = None
    data_type_output: T.Any = None
