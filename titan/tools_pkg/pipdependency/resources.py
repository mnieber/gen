import typing as T
from dataclasses import dataclass

from moonleap import Resource


@dataclass
class PipDependency(Resource):
    package_names: T.List[str]
    target: str


@dataclass
class PipRequirement(Resource):
    package_names: T.List[str]
    target: str
