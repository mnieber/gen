import typing as T
from dataclasses import dataclass

from moonleap.resource import Resource


@dataclass
class Flags(Resource):
    values: T.Dict[str, T.Union[str, bool]]
