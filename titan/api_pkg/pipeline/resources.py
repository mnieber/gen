import typing as T
from dataclasses import dataclass, field

from moonleap import Resource

from . import props


@dataclass
class Pipeline:
    name: str
    resources: T.List[Resource] = field(default_factory=list)

    def data_path(self, obj):
        return props.pipeline_data_path(self, obj)

    @property
    def source(self):
        return props.pipeline_source(self)


@dataclass
class PropsSource(Resource):
    pass


@dataclass
class LocalVars(Resource):
    pass
