import typing as T
from dataclasses import dataclass, field

from moonleap import Resource


@dataclass
class VsCodeProject(Resource):
    pass


@dataclass
class VsCodeProjectConfig(Resource):
    paths: T.List[str] = field(default_factory=list)
